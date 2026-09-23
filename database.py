"""
database.py
-----------
SQLite persistence layer for the IT Support Ticket System (Sprint 1).

Tables
------
  users            – registered users with roles
  tickets          – support tickets raised by employees
  issue_statistics – pre-seeded historical statistics
"""

import sqlite3
from datetime import datetime

DB_FILE = "tickets.db"


# ─────────────────────────────────────────────────────────────────────────────
#  Connection helper
# ─────────────────────────────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────────────────────────────────────
#  Initialisation
# ─────────────────────────────────────────────────────────────────────────────

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # ── Users table ──────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        )
    """)

    # Seed sample users only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ("john",     "employee123", "Employee"),
            ("alice",    "employee123", "Employee"),
            ("support1", "support123",  "IT Support"),
            ("support2", "support123",  "IT Support"),
            ("admin",    "admin123",    "Admin"),
        ]
        cursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            sample_users,
        )

    # ── Tickets table ─────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id         TEXT UNIQUE NOT NULL,
            employee_username TEXT NOT NULL,
            description       TEXT NOT NULL,
            category          TEXT NOT NULL,
            priority          TEXT NOT NULL,
            status            TEXT NOT NULL DEFAULT 'Open',
            created_at        TEXT NOT NULL,
            resolved_at       TEXT
        )
    """)

    # ── Issue statistics table ────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issue_statistics (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            category             TEXT UNIQUE NOT NULL,
            previous_occurrences INTEGER NOT NULL DEFAULT 0,
            recurring_cases      INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM issue_statistics")
    if cursor.fetchone()[0] == 0:
        fake_data = [
            ("WiFi Connectivity", 120, 30),
            ("Email Problem",      80, 12),
            ("Printer Problem",    60, 18),
            ("Password/Login",    100, 10),
            ("Software Problem",   90, 22),
            ("Hardware Problem",   70, 15),
            ("Unknown",            20,  4),
        ]
        cursor.executemany(
            "INSERT INTO issue_statistics (category, previous_occurrences, recurring_cases) VALUES (?, ?, ?)",
            fake_data,
        )

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  Authentication
# ─────────────────────────────────────────────────────────────────────────────

def authenticate_user(username: str, password: str):
    """
    Return the user row (dict) if credentials are valid, else None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ─────────────────────────────────────────────────────────────────────────────
#  User queries
# ─────────────────────────────────────────────────────────────────────────────

def get_all_users():
    """Return all users as a list of dicts (id, username, role)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
#  Ticket queries
# ─────────────────────────────────────────────────────────────────────────────

def get_next_ticket_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]
    conn.close()
    return f"TKT{1001 + count}"


def insert_ticket(ticket_id: str, employee_username: str,
                  description: str, category: str, priority: str):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """INSERT INTO tickets
           (ticket_id, employee_username, description, category, priority, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'Open', ?)""",
        (ticket_id, employee_username, description, category, priority, created_at),
    )
    conn.commit()
    conn.close()


def get_all_tickets():
    """Return all tickets (for IT Support / Admin views)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ticket_id, employee_username, category, priority, status "
        "FROM tickets ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ticket_by_id(ticket_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id.upper(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_ticket_status(ticket_id: str, new_status: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    resolved_at = None
    if new_status in ("Resolved", "Closed"):
        resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "UPDATE tickets SET status = ?, resolved_at = ? WHERE ticket_id = ?",
        (new_status, resolved_at, ticket_id.upper()),
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


# ─────────────────────────────────────────────────────────────────────────────
#  Statistics queries
# ─────────────────────────────────────────────────────────────────────────────

def get_all_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, previous_occurrences, recurring_cases "
        "FROM issue_statistics ORDER BY previous_occurrences DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_statistics_by_category(category: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, previous_occurrences, recurring_cases "
        "FROM issue_statistics WHERE category = ?",
        (category,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
