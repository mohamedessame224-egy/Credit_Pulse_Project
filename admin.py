"""
Credit Pulse - Admin Routes (plain sqlite3, session-based auth)
"""
import json
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash
from app import get_db
from utils.translations import get_lang, t, get_all_translations
from collections import defaultdict
from datetime import datetime, timedelta
import functools

admin_bp = Blueprint('admin', __name__)

# ── auth decorator ────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

# ── helpers ───────────────────────────────────────────────────

def get_current_admin(db):
    aid = session.get('admin_id')
    if not aid:
        return None
    return db.execute("SELECT * FROM admins WHERE id=?", (aid,)).fetchone()

def response_satisfaction(db, resp_id):
    rows = db.execute("""
        SELECT a.answer_value FROM answers a
        JOIN questions q ON q.id=a.question_id
        WHERE a.response_id=? AND q.question_type='rating'
    """, (resp_id,)).fetchall()
    vals = []
    for r in rows:
        try:
            vals.append(float(r['answer_value']))
        except Exception:
            pass
    return round(sum(vals)/len(vals), 2) if vals else None

# ── routes ────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    lang = get_lang()
    tr = get_all_translations()
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        db = get_db()
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        admin = db.execute("SELECT * FROM admins WHERE username=?", (username,)).fetchone()
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin['id']
            session['admin_name_ar'] = admin['name_ar']
            session['admin_name_en'] = admin['name_en']
            return redirect(url_for('admin.dashboard'))
        flash(t('admin_login_error'), 'error')

    return render_template('admin/login.html', lang=lang, tr=tr, t=t)


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    lang = get_lang()
    tr = get_all_translations()
    db = get_db()

    # Current admin for template
    current_user = {
        'name_ar': session.get('admin_name_ar', 'المدير'),
        'name_en': session.get('admin_name_en', 'Admin'),
    }

    survey = db.execute("SELECT * FROM surveys WHERE is_active=1 LIMIT 1").fetchone()
    survey = dict(survey) if survey else None

    all_resp = [dict(r) for r in db.execute("SELECT * FROM survey_responses").fetchall()]
    total = len(all_resp)
    dept_ids = set(r['department_id'] for r in all_resp if r['department_id'])
    dept_count = len(dept_ids)
    anon_count = sum(1 for r in all_resp if r['is_anonymous'])

    # Satisfaction scores
    scores = []
    for r in all_resp:
        s = response_satisfaction(db, r['id'])
        if s is not None:
            scores.append(s)
    avg_satisfaction = round(sum(scores)/len(scores), 2) if scores else 0
    pulse_score = round((avg_satisfaction / 5) * 100, 1)

    # Department data
    departments = [dict(d) for d in db.execute("SELECT * FROM departments ORDER BY id").fetchall()]
    dept_map = {d['id']: d for d in departments}
    dept_stats = {}
    for r in all_resp:
        did = r['department_id']
        if did and did in dept_map:
            key = did
            if key not in dept_stats:
                dept_stats[key] = {'count': 0, 'scores': [], 'dept': dept_map[did]}
            dept_stats[key]['count'] += 1
            s = response_satisfaction(db, r['id'])
            if s:
                dept_stats[key]['scores'].append(s)

    dept_data = []
    for did, info in dept_stats.items():
        avg = round(sum(info['scores'])/len(info['scores']), 2) if info['scores'] else 0
        dept_data.append({
            'name_ar': info['dept']['name_ar'],
            'name_en': info['dept']['name_en'],
            'count': info['count'],
            'avg': avg,
        })
    dept_data.sort(key=lambda x: x['count'], reverse=True)

    # 14-day trend
    today = datetime.utcnow().date()
    day_labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(13, -1, -1)]
    day_counts = defaultdict(int)
    for r in all_resp:
        try:
            day = r['submitted_at'][:10]
            day_counts[day] += 1
        except Exception:
            pass
    trend_data = [day_counts.get(d, 0) for d in day_labels]

    # Rating question stats
    question_stats = []
    if survey:
        for sec in db.execute("SELECT * FROM sections WHERE survey_id=? ORDER BY order_num", (survey['id'],)):
            for q in db.execute("SELECT * FROM questions WHERE section_id=? AND question_type='rating'", (sec['id'],)):
                rows = db.execute("SELECT answer_value FROM answers WHERE question_id=?", (q['id'],)).fetchall()
                vals = []
                for row in rows:
                    try:
                        vals.append(float(row['answer_value']))
                    except Exception:
                        pass
                avg_q = round(sum(vals)/len(vals), 2) if vals else 0
                text_ar = q['text_ar']
                text_en = q['text_en']
                question_stats.append({
                    'text_ar': (text_ar[:50]+'...') if len(text_ar)>50 else text_ar,
                    'text_en': (text_en[:50]+'...') if len(text_en)>50 else text_en,
                    'avg': avg_q,
                    'count': len(vals),
                })

    return render_template('admin/dashboard.html',
        lang=lang, tr=tr, t=t,
        current_user=current_user,
        survey=survey,
        total=total, dept_count=dept_count,
        anon_count=anon_count,
        avg_satisfaction=avg_satisfaction,
        pulse_score=pulse_score,
        dept_data=dept_data[:8],
        day_labels=json.dumps(day_labels),
        trend_data=json.dumps(trend_data),
        question_stats=question_stats,
        departments=departments,
    )


@admin_bp.route('/responses')
@login_required
def responses():
    lang = get_lang()
    tr = get_all_translations()
    db = get_db()
    current_user = {
        'name_ar': session.get('admin_name_ar', 'المدير'),
        'name_en': session.get('admin_name_en', 'Admin'),
    }
    survey = db.execute("SELECT * FROM surveys WHERE is_active=1 LIMIT 1").fetchone()
    survey = dict(survey) if survey else None
    all_responses = [dict(r) for r in db.execute(
        "SELECT * FROM survey_responses ORDER BY submitted_at DESC").fetchall()]
    departments = [dict(d) for d in db.execute("SELECT * FROM departments ORDER BY id").fetchall()]
    dept_map = {d['id']: d for d in departments}

    # Enrich with score and answers
    for resp in all_responses:
        resp['satisfaction_score'] = response_satisfaction(db, resp['id'])
        resp['answers_detail'] = []
        for a in db.execute("""SELECT a.*, q.text_ar, q.text_en, q.question_type
                FROM answers a JOIN questions q ON q.id=a.question_id
                WHERE a.response_id=?""", (resp['id'],)).fetchall():
            resp['answers_detail'].append(dict(a))

    return render_template('admin/responses.html',
        lang=lang, tr=tr, t=t,
        current_user=current_user,
        survey=survey,
        all_responses=all_responses,
        dept_map=dept_map)


@admin_bp.route('/survey-manager')
@login_required
def survey_manager():
    lang = get_lang()
    tr = get_all_translations()
    db = get_db()
    current_user = {
        'name_ar': session.get('admin_name_ar', 'المدير'),
        'name_en': session.get('admin_name_en', 'Admin'),
    }
    survey_row = db.execute("SELECT * FROM surveys WHERE is_active=1 LIMIT 1").fetchone()
    survey = None
    if survey_row:
        survey = dict(survey_row)
        survey['sections'] = []
        survey['responses_count'] = db.execute(
            "SELECT COUNT(*) FROM survey_responses WHERE survey_id=?", (survey['id'],)).fetchone()[0]
        for sec in db.execute("SELECT * FROM sections WHERE survey_id=? ORDER BY order_num", (survey['id'],)):
            s = dict(sec)
            s['questions'] = []
            for q in db.execute("SELECT * FROM questions WHERE section_id=? ORDER BY order_num", (s['id'],)):
                qd = dict(q)
                qd['answer_count'] = db.execute(
                    "SELECT COUNT(*) FROM answers WHERE question_id=?", (q['id'],)).fetchone()[0]
                if qd['options_ar']:
                    try:
                        qd['options_ar_list'] = json.loads(qd['options_ar'])
                    except Exception:
                        qd['options_ar_list'] = []
                if qd['options_en']:
                    try:
                        qd['options_en_list'] = json.loads(qd['options_en'])
                    except Exception:
                        qd['options_en_list'] = []
                s['questions'].append(qd)
            survey['sections'].append(s)

    return render_template('admin/survey_manager.html',
        lang=lang, tr=tr, t=t,
        current_user=current_user,
        survey=survey)
