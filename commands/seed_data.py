import sqlite3
from datetime import date, timedelta
import random

DB_NAME = "fintech_temp.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# -------------------------
# Customers
# -------------------------
customers = [
    ("Amit Sharma", "amit@gmail.com"),
    ("Priya Verma", "priya@gmail.com"),
    ("Rohit Mehta", "rohit@gmail.com"),
    ("Sneha Iyer", "sneha@gmail.com"),
    ("Vikas Patel", "vikas@gmail.com"),
    ("Neha Gupta", "neha@gmail.com"),
    ("Anil Kumar", "anil@gmail.com"),
    ("Pooja Nair", "pooja@gmail.com"),
    ("Rahul Singh", "rahul@gmail.com"),
    ("Kavita Joshi", "kavita@gmail.com"),
]

cursor.executemany("INSERT INTO customers (name, email) VALUES (?, ?)", customers)

# -------------------------
# Loans
# -------------------------
loans = [
    (1, "home_loan", "floating", 5200000, "2021-05-10", "active"),
    (2, "home_loan", "fixed", 4800000, "2020-03-15", "active"),
    (3, "home_loan", "floating", 6100000, "2019-08-01", "active"),
    (4, "personal_loan", "fixed", 800000, "2022-01-20", "active"),
    (5, "home_loan", "floating", 4500000, "2023-02-11", "active"),
    (6, "home_loan", "fixed", 7000000, "2018-11-09", "closed"),
    (7, "home_loan", "floating", 3900000, "2022-06-18", "active"),
    (8, "personal_loan", "fixed", 500000, "2021-09-25", "active"),
    (9, "home_loan", "floating", 5600000, "2020-12-30", "active"),
    (10, "home_loan", "fixed", 6200000, "2017-07-14", "active"),
]

cursor.executemany(
    """
INSERT INTO loans
(customer_id, loan_type, interest_type, amount, start_date, status)
VALUES (?, ?, ?, ?, ?, ?)
""",
    loans,
)

# -------------------------
# Complaints
# -------------------------
complaint_types = [
    "delay",
    "interest_rate",
    "foreclosure_charges",
    "documentation",
    "mis_selling",
]

statuses = ["open", "in_progress", "resolved"]

complaints = []

for i in range(1, 11):
    created_days_ago = random.randint(5, 45)
    created_at = date.today() - timedelta(days=created_days_ago)

    complaints.append(
        (
            i,  # customer_id
            i,  # loan_id
            random.choice(complaint_types),
            f"Customer raised issue related to {complaint_types[i % 5]}",
            random.choice(statuses),
            created_at.isoformat(),
            None,
        )
    )

cursor.executemany(
    """
INSERT INTO complaints
(customer_id, loan_id, complaint_type, description, status, created_at, resolved_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
""",
    complaints,
)

# -------------------------
# SLA Rules
# -------------------------
sla_rules = [
    ("home_loan", "delay", 30),
    ("home_loan", "interest_rate", 30),
    ("home_loan", "foreclosure_charges", 30),
    ("personal_loan", "delay", 15),
    ("personal_loan", "mis_selling", 15),
]

cursor.executemany(
    """
INSERT INTO sla_rules (product_type, complaint_type, max_resolution_days)
VALUES (?, ?, ?)
""",
    sla_rules,
)

# -------------------------
# Foreclosure Rules
# -------------------------
foreclosure_rules = [
    (
        "home_loan",
        "floating",
        1,
        0.0,
        "RBI Circular 2023 - No charges on floating rate",
    ),
    ("home_loan", "fixed", 1, 2.0, "Bank Policy - Fixed rate foreclosure"),
]

cursor.executemany(
    """
INSERT INTO foreclosure_rules
(loan_type, interest_type, foreclosure_allowed, charges_percentage, rule_reference)
VALUES (?, ?, ?, ?, ?)
""",
    foreclosure_rules,
)

# -------------------------
# Documents
# -------------------------
documents = [
    ("Home Loan Foreclosure Guidelines", "rbi", "RBI Circular 2023", "2023-08-01"),
    ("Customer Complaint Handling", "rbi", "RBI Ombudsman", "2022-04-01"),
    ("Insurance Claim Processing", "insurance", "IRDAI Policy", "2021-01-15"),
]

cursor.executemany(
    """
INSERT INTO documents
(doc_name, doc_type, source, effective_date)
VALUES (?, ?, ?, ?)
""",
    documents,
)

conn.commit()
conn.close()

print("✅ Inserted 10 customers with loans, complaints, SLA & rules")
