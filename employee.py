"""
Credit Pulse - Employee Routes (plain sqlite3)
"""
import json
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import get_db
from utils.translations import get_lang, t, get_all_translations

employee_bp = Blueprint('employee', __name__)

# ── helpers ──────────────────────────────────────────────────

def fetch_active_survey(db):
    row = db.execute("SELECT * FROM surveys WHERE is_active=1 LIMIT 1").fetchone()
    if not row:
        return None
    survey = dict(row)
    survey['sections'] = []
    for sec in db.execute("SELECT * FROM sections WHERE survey_id=? ORDER BY order_num", (survey['id'],)):
        s = dict(sec)
        s['questions'] = [dict(q) for q in db.execute(
            "SELECT * FROM questions WHERE section_id=? ORDER BY order_num", (s['id'],))]
        survey['sections'].append(s)
    return survey

def count_survey_questions(survey):
    return sum(len(s['questions']) for s in survey.get('sections', []))

# ── routes ───────────────────────────────────────────────────

@employee_bp.route('/')
def index():
    db = get_db()
    survey = fetch_active_survey(db)
    lang = get_lang()
    tr = get_all_translations()
    return render_template('employee/welcome.html', survey=survey, lang=lang, tr=tr, t=t)


@employee_bp.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in ['ar', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('employee.index'))


@employee_bp.route('/info', methods=['GET', 'POST'])
def info():
    db = get_db()
    survey = fetch_active_survey(db)
    if not survey:
        return redirect(url_for('employee.index'))

    departments = [dict(r) for r in db.execute("SELECT * FROM departments ORDER BY id")]
    lang = get_lang()
    tr = get_all_translations()

    if request.method == 'POST':
        dept_id = request.form.get('department_id')
        if not dept_id:
            flash(t('info_required'), 'error')
            return render_template('employee/info.html', survey=survey, departments=departments,
                                   lang=lang, tr=tr, t=t)
        is_anon = request.form.get('anonymous') == 'on'
        session['survey_info'] = {
            'survey_id': survey['id'],
            'dept_id': int(dept_id),
            'name': None if is_anon else request.form.get('name', '').strip() or None,
            'emp_id': None if is_anon else request.form.get('employee_id', '').strip() or None,
            'anonymous': is_anon,
        }
        return redirect(url_for('employee.survey_page', section_idx=0))

    return render_template('employee/info.html', survey=survey, departments=departments,
                           lang=lang, tr=tr, t=t)


@employee_bp.route('/survey/<int:section_idx>', methods=['GET', 'POST'])
def survey_page(section_idx):
    info = session.get('survey_info')
    if not info:
        return redirect(url_for('employee.index'))

    db = get_db()
    survey = fetch_active_survey(db)
    if not survey:
        return redirect(url_for('employee.index'))

    sections = survey['sections']
    lang = get_lang()
    tr = get_all_translations()

    if section_idx >= len(sections):
        return redirect(url_for('employee.submit'))

    if request.method == 'POST':
        answers = dict(session.get('answers', {}))
        section = sections[section_idx]
        for q in section['questions']:
            qkey = str(q['id'])
            if q['question_type'] == 'multiple_choice':
                answers[qkey] = json.dumps(request.form.getlist(f'q_{q["id"]}'))
            else:
                answers[qkey] = request.form.get(f'q_{q["id"]}', '')
        session['answers'] = answers
        session.modified = True

        if 'next' in request.form and section_idx + 1 < len(sections):
            return redirect(url_for('employee.survey_page', section_idx=section_idx + 1))
        elif 'prev' in request.form and section_idx > 0:
            return redirect(url_for('employee.survey_page', section_idx=section_idx - 1))
        else:
            return redirect(url_for('employee.submit'))

    section = sections[section_idx]
    total_q = count_survey_questions(survey)
    prev_q = sum(len(sections[i]['questions']) for i in range(section_idx))
    progress_pct = int(prev_q / total_q * 100) if total_q else 0
    saved_answers = session.get('answers', {})

    return render_template('employee/survey.html',
        survey=survey, section=section, sections=sections,
        section_idx=section_idx, total_sections=len(sections),
        progress_pct=progress_pct, lang=lang, tr=tr, t=t,
        saved_answers=saved_answers)


@employee_bp.route('/submit')
def submit():
    info = session.get('survey_info')
    answers_data = session.get('answers', {})
    if not info:
        return redirect(url_for('employee.index'))

    db = get_db()
    cur = db.execute("""INSERT INTO survey_responses
        (survey_id,department_id,employee_name,employee_id,is_anonymous,ip_address)
        VALUES (?,?,?,?,?,?)""", (
        info['survey_id'],
        info['dept_id'],
        info.get('name'),
        info.get('emp_id'),
        1 if info.get('anonymous') else 0,
        request.remote_addr,
    ))
    resp_id = cur.lastrowid

    for qid_str, val in answers_data.items():
        try:
            qid = int(qid_str)
            q = db.execute("SELECT question_type FROM questions WHERE id=?", (qid,)).fetchone()
            if not q:
                continue
            if q['question_type'] == 'multiple_choice':
                db.execute("INSERT INTO answers (response_id,question_id,answer_values) VALUES (?,?,?)",
                           (resp_id, qid, val))
            else:
                db.execute("INSERT INTO answers (response_id,question_id,answer_value) VALUES (?,?,?)",
                           (resp_id, qid, val))
        except Exception:
            pass

    db.commit()
    session.pop('survey_info', None)
    session.pop('answers', None)

    lang = get_lang()
    tr = get_all_translations()
    return render_template('employee/thanks.html', lang=lang, tr=tr, t=t)
