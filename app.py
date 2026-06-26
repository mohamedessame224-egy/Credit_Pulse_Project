"""
Credit Pulse - Application Factory
Uses only built-in sqlite3 (no Flask-SQLAlchemy needed)
"""
import os
import sqlite3
from flask import Flask, g

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'credit_pulse.db')

def get_db():
    if 'db' not in g:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'credit-pulse-nbe-secret-2024-xK9m'
    app.config['DATABASE'] = DATABASE

    app.teardown_appcontext(close_db)

    from routes.employee import employee_bp
    from routes.admin import admin_bp
    from routes.reports import reports_bp

    app.register_blueprint(employee_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    with app.app_context():
        from utils.init_db import initialize_db
        initialize_db()

    return app
