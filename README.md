# Week 5: Security Enhancements in Python Applications

A technical security audit, code hardening, and vulnerability remediation project demonstrating how to identify, exploit, and fix critical OWASP Top 10 security flaws in Python applications.

---

## 📌 Executive Summary

This project conducts a comprehensive security review of an insecure Python baseline application, identifies high-risk vulnerabilities—including SQL Injection (SQLi), OS Command Injection, Weak Password Cryptography (MD5), and Hardcoded Secrets—and refactors the code using enterprise-grade secure coding principles. Remediation efficacy was verified using automated `pytest` suites executed under Python 3.14.7.

---

## 🛡️ Vulnerability Audit & Remediation Matrix

| Vulnerability Category | CWE ID | Initial Risk | Remediation Implemented | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **SQL Injection (SQLi)** | [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | **CRITICAL** | Parameterized Queries (`?` placeholders) | **PASSED** (Payload Neutralized) |
| **OS Command Injection** | [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | **HIGH** | `subprocess.run(shell=False)` + Allowlist Regex | **PASSED** (Execution Blocked) |
| **Weak Hashing (MD5)** | [CWE-328](https://cwe.mitre.org/data/definitions/328.html) | **HIGH** | `bcrypt` Adaptive Hashing (Cost Factor 12) | **PASSED** (Salted Hash Generated) |
| **Hardcoded Secrets** | [CWE-798](https://cwe.mitre.org/data/definitions/798.html) | **MEDIUM** | Environment Variables (`os.getenv`) | **PASSED** (Secret Extracted) |

---

## 🔍 Code Hardening Breakdowns

### 1. SQL Injection Mitigation (`CWE-89`)
* **Vulnerable:** Direct string formatting allows syntax hijacking (`admin' OR '1'='1`).
  ```python
  # VULNERABLE
  cursor.execute(f"INSERT INTO users VALUES ('{username}', '{hashed_password}')")