"""
Credit Pulse - Main Entry Point
Registers template filters then starts the server
"""
import json
import webbrowser
import threading
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

# ── Template filters ──────────────────────────────────────────
@app.template_filter('from_json')
def from_json_filter(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except Exception:
        return []

@app.template_filter('max')
def max_filter(value, other=0):
    try:
        return max(int(value), int(other))
    except Exception:
        return other

# ── Start ─────────────────────────────────────────────────────
def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("=" * 60)
    print("  Credit Pulse - منصة استبيانات قطاع الائتمان")
    print("  البنك الأهلي المصري - National Bank of Egypt")
    print("=" * 60)
    print()
    print("  Starting server ...")
    print("  URL  : http://127.0.0.1:5000")
    print("  Admin: http://127.0.0.1:5000/admin")
    print()
    print("  Default Admin Login")
    print("  Username : admin")
    print("  Password : CreditPulse2024")
    print()
    print("  Press CTRL+C to stop")
    print("=" * 60)

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=False, host='127.0.0.1', port=5000)
