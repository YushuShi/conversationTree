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
            total_cost REAL DEFAULT 0.0,
            total_tokens INTEGER DEFAULT 0,
            openai_key TEXT,
            anthropic_key TEXT,
            google_key TEXT,
            tavily_key TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            session_id TEXT,
            cost REAL DEFAULT 0.0,
            tokens INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            email TEXT,
            title TEXT,
            tree_data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    check_and_migrate()

def check_and_migrate():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Check if total_tokens column exists
    c.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in c.fetchall()]
    
    if "total_tokens" not in columns:
        print("Migrating database: Adding total_tokens column to users table...")
        c.execute("ALTER TABLE users ADD COLUMN total_tokens INTEGER DEFAULT 0")
        
    if "openai_key" not in columns:
        print("Migrating database: Adding api key columns to users table...")
        c.execute("ALTER TABLE users ADD COLUMN openai_key TEXT")
        c.execute("ALTER TABLE users ADD COLUMN anthropic_key TEXT")
        c.execute("ALTER TABLE users ADD COLUMN google_key TEXT")
    if "tavily_key" not in columns:
        print("Migrating database: Adding tavily_key column to users table...")
        c.execute("ALTER TABLE users ADD COLUMN tavily_key TEXT")

    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            session_id TEXT,
            cost REAL DEFAULT 0.0,
            tokens INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        c.execute("INSERT INTO users (email, password_hash, total_cost, total_tokens) VALUES (?, ?, 0.0, 0)", 
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
    c.execute("SELECT email, total_cost, total_tokens FROM users WHERE email = ? AND password_hash = ?", 
              (email, hash_password(password)))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "email": row[0], 
            "total_cost": row[1],
            "total_tokens": row[2],
        }
    return None

def update_user_api_keys(email, openai_key, anthropic_key, google_key, tavily_key):
    # API keys are intentionally not stored server-side.
    return

def update_user_stats(email, cost_increment, token_increment):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET total_cost = total_cost + ?, total_tokens = total_tokens + ? WHERE email = ?", 
              (cost_increment, token_increment, email))
    conn.commit()
    conn.close()

def log_usage(email, cost_increment, token_increment, session_id, created_at_iso):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO usage_log (email, session_id, cost, tokens, created_at) VALUES (?, ?, ?, ?, ?)",
        (email, session_id, cost_increment, token_increment, created_at_iso),
    )
    conn.commit()
    conn.close()

def get_usage_rollups(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND date(created_at, 'localtime') = date('now', 'localtime')
        """,
        (email,),
    )
    daily_cost, daily_tokens = c.fetchone()
    c.execute(
        """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND date(created_at, 'localtime') >= date('now', '-6 days', 'localtime')
        """,
        (email,),
    )
    weekly_cost, weekly_tokens = c.fetchone()
    conn.close()
    return {
        "daily_cost": daily_cost,
        "daily_tokens": daily_tokens,
        "weekly_cost": weekly_cost,
        "weekly_tokens": weekly_tokens,
    }

def get_user_cost(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT total_cost FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0.0

import json
import uuid
import datetime
from .classes import ChatNode, build_tree_dict, flatten_tree

def save_conversation(email, nodes_map, root_id, touch_updated_at: bool = True):
    """
    Saves a conversation tree to the database for a user.
    If the root_id already exists for this user, update it.
    Otherwise create a new entry.
    """
    # Convert flat map back to nested dict for storage
    tree_data = build_tree_dict(nodes_map, root_id)
    
    # We use the root node's ID as the conversation ID for simplicity
    # or we can check if it exists.
    # The 'conversations' table has: id, user_id, title, root_data, created_at, updated_at
    # Actually wait, `ChatNode` object has `id`.
    
    # Title is the first user message content (truncated)
    title = "New Chat"
    root_node = nodes_map.get(root_id)
    if root_node:
        # Find first user child
        # This logic requires traversal.
        # Simple for now: just use root content if it's user (it's usually system)
        pass

    # Basic Save Implementation
    with sqlite3.connect("chat_users.db") as conn:
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute("SELECT id FROM conversations WHERE id = ? AND email = ?", (root_id, email))
        exists = cursor.fetchone()
        
        json_data = json.dumps(tree_data)
        now = datetime.datetime.now().isoformat()
        
        if exists:
            if touch_updated_at:
                cursor.execute(
                    "UPDATE conversations SET tree_data = ?, updated_at = ? WHERE id = ?",
                    (json_data, now, root_id),
                )
            else:
                cursor.execute(
                    "UPDATE conversations SET tree_data = ? WHERE id = ?",
                    (json_data, root_id),
                )
        else:
            # Generate a title
            # Search for first user message
            title = "Conversation"
            # Traverse a bit? 
            # root_node -> children.
            if root_node:
                for child_id in root_node.children_ids:
                    child = nodes_map.get(child_id)
                    if child and child.role == "user":
                        title = child.content[:30]
                        break
            
            cursor.execute("INSERT INTO conversations (id, email, title, tree_data, updated_at) VALUES (?, ?, ?, ?, ?)",
                           (root_id, email, title, json_data, now))
        conn.commit()

def get_user_conversations(email):
    with sqlite3.connect("chat_users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, updated_at, tree_data FROM conversations WHERE email = ? ORDER BY updated_at DESC",
            (email,),
        )
        rows = cursor.fetchall()
        filtered = []
        for cid, title, updated_at, tree_data in rows:
            try:
                data = json.loads(tree_data) if tree_data else {}
            except json.JSONDecodeError:
                data = {}
            if _conversation_has_user_input(data):
                filtered.append((cid, title, updated_at))
        return filtered


def _conversation_has_user_input(tree_data: dict) -> bool:
    """Return True when a conversation contains a non-empty user message."""
    if not tree_data:
        return False
    stack = [tree_data]
    while stack:
        node = stack.pop()
        if node.get("role") == "user" and node.get("content", "").strip():
            return True
        stack.extend(node.get("children", []))
    return False


def load_conversation(cid):
    with sqlite3.connect("chat_users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tree_data FROM conversations WHERE id = ?", (cid,))
        row = cursor.fetchone()
        if row:
            data = json.loads(row[0])
            # Return flattened dict
            return flatten_tree(data)
    return None


def delete_conversation(email, chat_id):
    with sqlite3.connect("chat_users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM conversations WHERE id = ? AND email = ?",
            (chat_id, email),
        )
        conn.commit()
