import sqlite3

DB_NAME = "fintech_temp.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # ---- Customers ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # ---- Loans ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        loan_type TEXT CHECK(loan_type IN ('home_loan', 'personal_loan')),
        interest_type TEXT CHECK(interest_type IN ('fixed', 'floating')),
        amount REAL,
        start_date DATE,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """
    )

    # ---- Complaints ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        loan_id INTEGER,
        complaint_type TEXT,
        description TEXT,
        status TEXT CHECK(status IN ('open', 'in_progress', 'resolved')),
        created_at DATE,
        resolved_at DATE,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(loan_id) REFERENCES loans(id)
    )
    """
    )

    # ---- SLA Rules ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS sla_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_type TEXT,
        complaint_type TEXT,
        max_resolution_days INTEGER
    )
    """
    )

    # ---- Foreclosure Rules ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS foreclosure_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_type TEXT,
        interest_type TEXT,
        foreclosure_allowed BOOLEAN,
        charges_percentage REAL,
        rule_reference TEXT
    )
    """
    )

    # ---- Documents (RAG grounding) ----
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_name TEXT,
        doc_type TEXT,
        source TEXT,
        effective_date DATE
    )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("✅ Database & tables created")
