import sqlite3
import hashlib
import os

# VULNERABILITY 1: Hardcoded Sensitive API Key
API_SECRET_KEY = "super_secret_admin_key_12345"

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def register_user_vulnerable(username, password):
    # VULNERABILITY 2: Weak Cryptographic Hashing (MD5)
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # VULNERABILITY 3: SQL Injection via String Formatting
    query = f"INSERT INTO users VALUES ('{username}', '{hashed_password}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

def ping_host_vulnerable(hostname):
    # VULNERABILITY 4: Command Injection via OS System Call
    os.system(f"ping -c 1 {hostname}")