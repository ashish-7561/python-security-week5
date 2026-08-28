import sqlite3
import bcrypt
import subprocess
import os
import shlex
from typing import Optional

# FIX 1: Environment Variable Injection for Secrets
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default_fallback_development_key")

def init_db():
    conn = sqlite3.connect("secure_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user_secure(username: str, password: str) -> bool:
    # FIX 2: Secure Password Hashing using bcrypt with Salt
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    conn = sqlite3.connect("secure_users.db")
    cursor = conn.cursor()
    try:
        # FIX 3: Parameterized Queries (Prevents SQL Injection)
        query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def ping_host_secure(hostname: str) -> bool:
    # FIX 4: Secure Subprocess Execution with Input Sanitization & Array Passing
    # Avoids shell=True to neutralize command injection payloads
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    if not set(hostname).issubset(allowed_chars):
        raise ValueError("Invalid hostname character sequence detected.")

    cmd = ["ping", "-c", "1", hostname]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return result.returncode == 0