import pytest
import sqlite3
import os
from secure_app import register_user_secure, ping_host_secure, init_db

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield
    if os.path.exists("secure_users.db"):
        os.remove("secure_users.db")

def test_sql_injection_mitigation():
    # Attempt SQL Injection Payload as Username
    sqli_payload = "admin' OR '1'='1"
    success = register_user_secure(sqli_payload, "SecurePassword123!")
    assert success is True
    
    # Query database to ensure payload was literal, not executed as SQL
    conn = sqlite3.connect("secure_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (sqli_payload,))
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[0] == "admin' OR '1'='1"

def test_command_injection_mitigation():
    # Attempt Command Injection Payload
    cmd_payload = "127.0.0.1; cat /etc/passwd"
    with pytest.raises(ValueError, match="Invalid hostname character sequence detected."):
        ping_host_secure(cmd_payload)