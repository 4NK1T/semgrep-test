# Sample Python app — intentionally has security issues for Semgrep to catch

import sqlite3
import subprocess
import hashlib

# Hardcoded secret (Semgrep: secrets rule)
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "supersecret123"

def get_user(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # SQL injection: user input concatenated directly (Semgrep: security-audit)
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

def run_command(user_input):
    # Command injection: unsanitized input passed to shell (Semgrep: security-audit)
    result = subprocess.run(user_input, shell=True, capture_output=True)
    return result.stdout

def hash_password(password):
    # Weak hashing algorithm: MD5 (Semgrep: security-audit)
    return hashlib.md5(password.encode()).hexdigest()

def get_admin(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Another SQL injection
    cursor.execute("SELECT * FROM admins WHERE username = '%s'" % username)
    return cursor.fetchone()
