"""
Credit Pulse - Seed Demo Data (plain sqlite3)
Run:  python utils/seed_demo.py
"""
import sys, os, random, json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'credit_pulse.db')

def seed():
    import sqlite3
    if not os.path.exists(DATABASE):
        print("Database not found. Run: python run.py  first.")
        return

    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    survey = con.execute("SELECT * FROM surveys WHERE is_active=1 LIMIT 1").fetchone()
    if not survey:
        print("No active survey. Start the app first."); return

    departments = con.execute("SELECT * FROM departments").fetchall()
    questions = con.execute("SELECT * FROM questions").fetchall()

    existing = con.execute("SELECT COUNT(*) FROM survey_responses").fetchone()[0]
    if existing >= 30:
        print(f"Already have {existing} responses. Skipping."); return

    NAMES = ['أحمد محمد','سارة أحمد','محمد علي','منى حسن','خالد إبراهيم',
             'فاطمة محمود','عمر عبدالله','نور الدين','ياسمين طارق','حسام رضا',
             'دينا سمير','علي حسن','رنا مصطفى','كريم وليد','هبة الله',
             'أيمن صبري','لمياء عادل','تامر جمال','غادة فاروق','إيهاب ناصر']
    COMMENTS = [
        'بيئة العمل ممتازة وتحتاج إلى مزيد من التطوير.',
        'نرجو تحسين آليات التواصل بين الأقسام.',
        'الإدارة داعمة ومتعاونة بشكل جيد.',
        'نحتاج إلى برامج تدريبية أكثر تخصصاً.',
        'العمل الجماعي ممتاز والروح الإيجابية واضحة.',
        '',
    ]

    count = 0
    for dept in departments:
        for _ in range(random.randint(3, 8)):
            is_anon = random.random() < 0.35
            name = None if is_anon else random.choice(NAMES)
            emp_id = None if is_anon else f"NBE{random.randint(10000,99999)}"
            dt = (datetime.utcnow() - timedelta(days=random.randint(0,14),
                  hours=random.randint(0,8), minutes=random.randint(0,59))).strftime('%Y-%m-%d %H:%M:%S')
            cur = con.execute("""INSERT INTO survey_responses
                (survey_id,department_id,employee_name,employee_id,is_anonymous,submitted_at,ip_address)
                VALUES (?,?,?,?,?,?,?)""",
                (survey['id'], dept['id'], name, emp_id, 1 if is_anon else 0, dt, '127.0.0.1'))
            rid = cur.lastrowid

            for q in questions:
                if q['question_type'] == 'rating':
                    val = str(random.choices([3,4,4,5,5], weights=[1,2,3,3,1])[0])
                    con.execute("INSERT INTO answers (response_id,question_id,answer_value) VALUES (?,?,?)",
                                (rid, q['id'], val))
                elif q['question_type'] == 'single_choice':
                    try:
                        opts = json.loads(q['options_ar'] or '[]')
                        if opts:
                            con.execute("INSERT INTO answers (response_id,question_id,answer_value) VALUES (?,?,?)",
                                        (rid, q['id'], random.choice(opts)))
                    except Exception:
                        pass
                elif q['question_type'] == 'multiple_choice':
                    try:
                        opts = json.loads(q['options_ar'] or '[]')
                        if opts:
                            chosen = random.sample(opts, k=random.randint(1, min(3, len(opts))))
                            con.execute("INSERT INTO answers (response_id,question_id,answer_values) VALUES (?,?,?)",
                                        (rid, q['id'], json.dumps(chosen)))
                    except Exception:
                        pass
                elif q['question_type'] == 'text':
                    val = random.choice(COMMENTS)
                    if val:
                        con.execute("INSERT INTO answers (response_id,question_id,answer_value) VALUES (?,?,?)",
                                    (rid, q['id'], val))
            count += 1

    con.commit()
    con.close()
    print(f"  [OK] Seeded {count} demo responses.")

if __name__ == '__main__':
    seed()
