"""
Credit Pulse - Database Models
"""
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name_ar = db.Column(db.String(120), default='المدير')
    name_en = db.Column(db.String(120), default='Administrator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    title_ar = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    estimated_minutes = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sections = db.relationship('Section', backref='survey', lazy=True, cascade='all, delete-orphan', order_by='Section.order_num')
    responses = db.relationship('SurveyResponse', backref='survey', lazy=True, cascade='all, delete-orphan')


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    title_ar = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    order_num = db.Column(db.Integer, default=0)
    questions = db.relationship('Question', backref='section', lazy=True, cascade='all, delete-orphan', order_by='Question.order_num')


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    text_ar = db.Column(db.Text, nullable=False)
    text_en = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), nullable=False)  # single_choice, multiple_choice, rating, text
    options_ar = db.Column(db.Text)  # JSON string
    options_en = db.Column(db.Text)  # JSON string
    is_required = db.Column(db.Boolean, default=True)
    order_num = db.Column(db.Integer, default=0)
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    responses = db.relationship('SurveyResponse', backref='department', lazy=True)


class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    employee_name = db.Column(db.String(150))
    employee_id = db.Column(db.String(50))
    is_anonymous = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    answers = db.relationship('Answer', backref='response', lazy=True, cascade='all, delete-orphan')

    @property
    def satisfaction_score(self):
        rating_answers = [a for a in self.answers if a.question and a.question.question_type == 'rating']
        if not rating_answers:
            return None
        total = 0
        count = 0
        for a in rating_answers:
            try:
                val = float(a.answer_value)
                total += val
                count += 1
            except:
                pass
        return round(total / count, 2) if count > 0 else None


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('survey_responses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_value = db.Column(db.Text)  # For single/text answers
    answer_values = db.Column(db.Text)  # JSON for multiple choice
