import os
import sqlite3
import hashlib
import json
import datetime
from typing import Optional

try:
    import psycopg2
except ModuleNotFoundError:
    psycopg2 = None

from .classes import build_tree_dict, flatten_tree

DB_NAME = "chat_users.db"
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USE_POSTGRES = DATABASE_URL.startswith("postgres")


def _format_query(query: str) -> str:
    if USE_POSTGRES:
        return query.replace("?", "%s")
    return query


def _connect():
    if USE_POSTGRES:
        if psycopg2 is None:
            raise RuntimeError("psycopg2 is required for DATABASE_URL usage.")
        return psycopg2.connect(DATABASE_URL)
    return sqlite3.connect(DB_NAME)


def _execute(query: str, params: tuple = (), fetch: Optional[str] = None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(_format_query(query), params)
        if fetch == "one":
            return cursor.fetchone()
        if fetch == "all":
            return cursor.fetchall()
        return None


def init_db():
    if USE_POSTGRES:
        _init_postgres()
    else:
        _init_sqlite()


def _init_sqlite():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            total_cost REAL DEFAULT 0.0,
            total_tokens INTEGER DEFAULT 0
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            session_id TEXT,
            cost REAL DEFAULT 0.0,
            tokens INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            email TEXT,
            title TEXT,
            tree_data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()
    check_and_migrate()


def _init_postgres():
    _execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            total_cost REAL DEFAULT 0.0,
            total_tokens INTEGER DEFAULT 0
        )
        """
    )
    _execute(
        """
        CREATE TABLE IF NOT EXISTS usage_log (
            id SERIAL PRIMARY KEY,
            email TEXT,
            session_id TEXT,
            cost REAL DEFAULT 0.0,
            tokens INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    _execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            email TEXT,
            title TEXT,
            tree_data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    _execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS total_tokens INTEGER DEFAULT 0"
    )


def check_and_migrate():
    if USE_POSTGRES:
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in c.fetchall()]

    if "total_tokens" not in columns:
        print("Migrating database: Adding total_tokens column to users table...")
        c.execute("ALTER TABLE users ADD COLUMN total_tokens INTEGER DEFAULT 0")

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            session_id TEXT,
            cost REAL DEFAULT 0.0,
            tokens INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(email, password):
    try:
        _execute(
            "INSERT INTO users (email, password_hash, total_cost, total_tokens) VALUES (?, ?, 0.0, 0)",
            (email, hash_password(password)),
        )
        return True
    except Exception:
        return False


def authenticate_user(email, password):
    row = _execute(
        "SELECT email, total_cost, total_tokens FROM users WHERE email = ? AND password_hash = ?",
        (email, hash_password(password)),
        fetch="one",
    )
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
    _execute(
        "UPDATE users SET total_cost = total_cost + ?, total_tokens = total_tokens + ? WHERE email = ?",
        (cost_increment, token_increment, email),
    )


def log_usage(email, cost_increment, token_increment, session_id, created_at_iso):
    _execute(
        "INSERT INTO usage_log (email, session_id, cost, tokens, created_at) VALUES (?, ?, ?, ?, ?)",
        (email, session_id, cost_increment, token_increment, created_at_iso),
    )


def get_usage_rollups(email):
    if USE_POSTGRES:
        daily_query = """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND created_at::date = CURRENT_DATE
        """
        weekly_query = """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND created_at::date >= CURRENT_DATE - INTERVAL '6 days'
        """
    else:
        daily_query = """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND date(created_at, 'localtime') = date('now', 'localtime')
        """
        weekly_query = """
        SELECT
            COALESCE(SUM(cost), 0.0),
            COALESCE(SUM(tokens), 0)
        FROM usage_log
        WHERE email = ?
          AND date(created_at, 'localtime') >= date('now', '-6 days', 'localtime')
        """

    daily = _execute(daily_query, (email,), fetch="one")
    weekly = _execute(weekly_query, (email,), fetch="one")
    daily_cost, daily_tokens = daily or (0.0, 0)
    weekly_cost, weekly_tokens = weekly or (0.0, 0)
    return {
        "daily_cost": daily_cost,
        "daily_tokens": daily_tokens,
        "weekly_cost": weekly_cost,
        "weekly_tokens": weekly_tokens,
    }


def get_user_cost(email):
    row = _execute(
        "SELECT total_cost FROM users WHERE email = ?",
        (email,),
        fetch="one",
    )
    return row[0] if row else 0.0


def save_conversation(email, nodes_map, root_id, touch_updated_at: bool = True):
    """
    Saves a conversation tree to the database for a user.
    If the root_id already exists for this user, update it.
    Otherwise create a new entry.
    """
    tree_data = build_tree_dict(nodes_map, root_id)
    title = "New Chat"
    root_node = nodes_map.get(root_id)
    if root_node:
        pass

    row = _execute(
        "SELECT id FROM conversations WHERE id = ? AND email = ?",
        (root_id, email),
        fetch="one",
    )
    exists = row is not None
    json_data = json.dumps(tree_data)
    now = datetime.datetime.now().isoformat()

    if exists:
        if touch_updated_at:
            _execute(
                "UPDATE conversations SET tree_data = ?, updated_at = ? WHERE id = ?",
                (json_data, now, root_id),
            )
        else:
            _execute(
                "UPDATE conversations SET tree_data = ? WHERE id = ?",
                (json_data, root_id),
            )
    else:
        title = "Conversation"
        if root_node:
            for child_id in root_node.children_ids:
                child = nodes_map.get(child_id)
                if child and child.role == "user":
                    title = child.content[:30]
                    break
        _execute(
            "INSERT INTO conversations (id, email, title, tree_data, updated_at) VALUES (?, ?, ?, ?, ?)",
            (root_id, email, title, json_data, now),
        )


def get_user_conversations(email):
    rows = _execute(
        "SELECT id, title, updated_at, tree_data FROM conversations WHERE email = ? ORDER BY updated_at DESC",
        (email,),
        fetch="all",
    )
    rows = rows or []
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
    row = _execute(
        "SELECT tree_data FROM conversations WHERE id = ?",
        (cid,),
        fetch="one",
    )
    if row:
        data = json.loads(row[0])
        return flatten_tree(data)
    return None


def delete_conversation(email, chat_id):
    _execute(
        "DELETE FROM conversations WHERE id = ? AND email = ?",
        (chat_id, email),
    )
