import sqlite3
import hashlib

DB_NAME = "chat_users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            total_cost REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password_hash, total_cost) VALUES (?, ?, 0.0)", 
                  (email, hash_password(password)))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def authenticate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT email, total_cost FROM users WHERE email = ? AND password_hash = ?", 
              (email, hash_password(password)))
    row = c.fetchone()
    conn.close()
    if row:
        return {"email": row[0], "total_cost": row[1]}
    return None

def update_user_cost(email, cost_increment):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET total_cost = total_cost + ? WHERE email = ?", (cost_increment, email))
    conn.commit()
    conn.close()

def get_user_cost(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT total_cost FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0.0