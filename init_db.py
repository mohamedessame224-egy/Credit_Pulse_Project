"""
Credit Pulse - Database Initialization (plain sqlite3)
"""
import sqlite3, os, json
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'credit_pulse.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name_ar TEXT DEFAULT 'مدير النظام',
    name_en TEXT DEFAULT 'System Administrator'
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_ar TEXT NOT NULL,
    title_en TEXT NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    is_active INTEGER DEFAULT 1,
    estimated_minutes INTEGER DEFAULT 10
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER NOT NULL,
    title_ar TEXT NOT NULL,
    title_en TEXT NOT NULL,
    order_num INTEGER DEFAULT 0,
    FOREIGN KEY(survey_id) REFERENCES surveys(id)
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    text_ar TEXT NOT NULL,
    text_en TEXT NOT NULL,
    question_type TEXT NOT NULL,
    options_ar TEXT,
    options_en TEXT,
    is_required INTEGER DEFAULT 1,
    order_num INTEGER DEFAULT 0,
    FOREIGN KEY(section_id) REFERENCES sections(id)
);

CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER NOT NULL,
    department_id INTEGER,
    employee_name TEXT,
    employee_id TEXT,
    is_anonymous INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    FOREIGN KEY(survey_id) REFERENCES surveys(id),
    FOREIGN KEY(department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer_value TEXT,
    answer_values TEXT,
    FOREIGN KEY(response_id) REFERENCES survey_responses(id),
    FOREIGN KEY(question_id) REFERENCES questions(id)
);
"""

DEPARTMENTS = [
    ('إدارة الائتمان', 'Credit Management'),
    ('إدارة المخاطر', 'Risk Management'),
    ('الائتمان التجاري', 'Commercial Credit'),
    ('الائتمان الاستهلاكي', 'Consumer Credit'),
    ('الائتمان العقاري', 'Mortgage Credit'),
    ('متابعة الديون المشكوك فيها', 'Non-Performing Loans'),
    ('تحليل الائتمان', 'Credit Analysis'),
    ('الرقابة والامتثال', 'Compliance & Control'),
    ('تكنولوجيا المعلومات', 'Information Technology'),
    ('الموارد البشرية', 'Human Resources'),
]

def initialize_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    con = sqlite3.connect(DATABASE)
    con.executescript(SCHEMA)

    # Admin
    if not con.execute("SELECT id FROM admins LIMIT 1").fetchone():
        pw = generate_password_hash('CreditPulse2024')
        con.execute("INSERT INTO admins (username,password_hash) VALUES (?,?)", ('admin', pw))
        print("  [OK] Default admin: admin / CreditPulse2024")

    # Departments
    if not con.execute("SELECT id FROM departments LIMIT 1").fetchone():
        con.executemany("INSERT INTO departments (name_ar,name_en) VALUES (?,?)", DEPARTMENTS)
        print("  [OK] 10 departments created")

    # Survey
    if not con.execute("SELECT id FROM surveys LIMIT 1").fetchone():
        cur = con.execute("""INSERT INTO surveys (title_ar,title_en,description_ar,description_en,estimated_minutes)
            VALUES (?,?,?,?,?)""", (
            'استبيان قياس رضا موظفي قطاع الائتمان',
            'Credit Sector Employee Satisfaction Survey',
            'نسعى من خلال هذا الاستبيان إلى قياس مستوى رضا الموظفين وتحديد مجالات التحسين في قطاع الائتمان بالبنك الأهلي المصري.',
            'This survey aims to measure employee satisfaction levels and identify areas for improvement in the Credit Sector of the National Bank of Egypt.',
            10,
        ))
        sid = cur.lastrowid

        sections_data = [
            ('بيئة العمل', 'Work Environment', [
                ('كيف تقيم بيئة العمل العامة في قسمك؟', 'How do you rate the overall work environment in your department?', 'rating', None, None),
                ('كيف تقيم مستوى التواصل والتعاون بين الأقسام؟', 'How do you rate communication and collaboration between departments?', 'single_choice',
                 json.dumps(['ممتاز','جيد جداً','جيد','يحتاج تحسين','ضعيف']),
                 json.dumps(['Excellent','Very Good','Good','Needs Improvement','Poor'])),
                ('ما هي أبرز التحديات التي تواجهها في بيئة العمل؟', 'What are the main challenges you face in the work environment?', 'multiple_choice',
                 json.dumps(['ضغط العمل','قلة الموارد','ضعف التواصل','التحديات التقنية','العلاقة مع الإدارة','أخرى']),
                 json.dumps(['Work Pressure','Lack of Resources','Poor Communication','Technical Challenges','Management Relations','Other'])),
            ]),
            ('القيادة والإدارة', 'Leadership & Management', [
                ('كيف تقيم كفاءة مديرك المباشر في إدارة الفريق؟', "How do you rate your direct manager's effectiveness in leading the team?", 'rating', None, None),
                ('هل تشعر أن ملاحظاتك وأفكارك يتم الاستماع إليها من قبل الإدارة؟', 'Do you feel that your feedback and ideas are heard by management?', 'single_choice',
                 json.dumps(['دائماً','غالباً','أحياناً','نادراً','أبداً']),
                 json.dumps(['Always','Often','Sometimes','Rarely','Never'])),
                ('ما تعليقك على أسلوب القيادة في قسمك؟', 'What are your comments on the leadership style in your department?', 'text', None, None),
            ]),
            ('التطوير المهني', 'Professional Development', [
                ('كيف تقيم فرص التدريب والتطوير المتاحة لك؟', 'How do you rate the training and development opportunities available to you?', 'rating', None, None),
                ('ما أنواع التدريب التي تحتاجها أكثر؟', 'What types of training do you need most?', 'multiple_choice',
                 json.dumps(['مهارات تقنية','مهارات قيادية','تحليل الائتمان','مهارات التواصل','إدارة المخاطر','الامتثال والتشريعات']),
                 json.dumps(['Technical Skills','Leadership Skills','Credit Analysis','Communication Skills','Risk Management','Compliance & Regulations'])),
                ('كيف تقيم مستوى رضاك الوظيفي بشكل عام؟', 'How do you rate your overall job satisfaction?', 'rating', None, None),
            ]),
            ('عمليات الائتمان', 'Credit Operations', [
                ('كيف تقيم كفاءة الإجراءات والعمليات الائتمانية الحالية؟', 'How do you rate the efficiency of current credit procedures and processes?', 'rating', None, None),
                ('ما التحسينات التي تقترحها لتطوير عمليات الائتمان؟', 'What improvements do you suggest for credit operations development?', 'text', None, None),
            ]),
        ]

        for s_idx, (s_ar, s_en, qs) in enumerate(sections_data, 1):
            scur = con.execute("INSERT INTO sections (survey_id,title_ar,title_en,order_num) VALUES (?,?,?,?)",
                               (sid, s_ar, s_en, s_idx))
            sec_id = scur.lastrowid
            for q_idx, (q_ar, q_en, qtype, opts_ar, opts_en) in enumerate(qs, 1):
                con.execute("""INSERT INTO questions
                    (section_id,text_ar,text_en,question_type,options_ar,options_en,is_required,order_num)
                    VALUES (?,?,?,?,?,?,?,?)""",
                    (sec_id, q_ar, q_en, qtype, opts_ar, opts_en, 1, q_idx))

        print("  [OK] Sample survey created: 4 sections, 11 questions")

    con.commit()
    con.close()
