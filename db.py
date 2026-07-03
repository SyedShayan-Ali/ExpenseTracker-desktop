import sqlite3
from config import DEFAULT_BUDGET, DEFAULT_CURRENCY


DB_NAME = "expense_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    """)

    # Settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            monthly_budget REAL DEFAULT 0,
            currency_symbol TEXT DEFAULT 'Rs.',
            theme_mode TEXT DEFAULT 'dark'
        )
    """)

    # Add theme_mode column if it doesn't already exist
    cursor.execute("PRAGMA table_info(settings)")
    columns = [column[1] for column in cursor.fetchall()]

    if "theme_mode" not in columns:
        cursor.execute("ALTER TABLE settings ADD COLUMN theme_mode TEXT DEFAULT 'dark'")

    # Make sure one settings row always exists
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO settings (id, monthly_budget, currency_symbol, theme_mode)
            VALUES (?, ?, ?, ?)
        """, (1, DEFAULT_BUDGET, DEFAULT_CURRENCY, "dark"))

    conn.commit()
    conn.close()


def add_transaction(txn_type, amount, category, date, note):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (type, amount, category, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (txn_type, amount, category, date, note))

    conn.commit()
    conn.close()


def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, amount, category, date, note
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

    conn.commit()
    conn.close()


def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    # Total income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
    total_income = cursor.fetchone()[0]
    if total_income is None:
        total_income = 0

    # Total expense
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
    total_expense = cursor.fetchone()[0]
    if total_expense is None:
        total_expense = 0

    # This month expense
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'Expense'
        AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)
    this_month_expense = cursor.fetchone()[0]
    if this_month_expense is None:
        this_month_expense = 0

    conn.close()

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "this_month_expense": this_month_expense
    }


def get_recent_transactions(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, amount, category, date, note
        FROM transactions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_settings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_budget, currency_symbol, theme_mode
        FROM settings
        WHERE id = 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "monthly_budget": row[0],
            "currency_symbol": row[1],
            "theme_mode": row[2]
        }

    return {
        "monthly_budget": 0,
        "currency_symbol": "Rs.",
        "theme_mode": "dark"
    }


def save_settings(monthly_budget, currency_symbol, theme_mode):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE settings
        SET monthly_budget = ?, currency_symbol = ?, theme_mode = ?
        WHERE id = 1
    """, (monthly_budget, currency_symbol, theme_mode))

    conn.commit()
    conn.close()