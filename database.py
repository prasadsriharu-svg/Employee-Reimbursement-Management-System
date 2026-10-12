import sqlite3
from auth_service import hash_password

def create_table():
    connection = sqlite3.connect("reimbursement.db")
    connection.execute("""CREATE TABLE IF NOT EXISTS claims(
    id INTEGER PRIMARY KEY,
    employee_name TEXT,
    amount REAL,
    category TEXT,
    description TEXT,
    receipt TEXT,
    status TEXT)""")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS category_limits (
            category_id INTEGER PRIMARY KEY,
            max_amount REAL NOT NULL CHECK(max_amount > 0),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    connection.commit()
    connection.close()


create_table()


###################
#   Users Table   #
###################

def create_user(employee_name, username, password, role):
    password_hash = hash_password(password)

    connection = sqlite3.connect("reimbursement.db")

    connection.execute("""
    INSERT INTO users
    (employee_name, username, password_hash, role)
    VALUES(?,?,?,?)""",
    (employee_name, username, password_hash, role))
    connection.commit()
    connection.close()

def get_user_by_username(username):
    connection = sqlite3.connect("reimbursement.db")

    cursor = connection.execute("""
        SELECT id, employee_name, username, password_hash, role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return None

    return {
        "id": user[0],
        "employee_name": user[1],
        "username": user[2],
        "password_hash": user[3],
        "role": user[4]
    }



###################
#   Claim Table   #
###################

def insert_claim(employee_name, amount, category, description, receipt, status):
    connection = sqlite3.connect("reimbursement.db")
    connection.execute("""
    INSERT INTO claims
    (employee_name, amount, category, description, receipt, status)
    VALUES (?,?,?,?,?,?)""",
    (employee_name, amount, category, description, receipt, status))
    connection.commit()
    connection.close()
def insert_claim_with_receipt(
    employee_name,
    amount,
    category,
    description,
    receipt_filename,
    employee_id
):
    connection = sqlite3.connect("reimbursement.db")

    try:
        connection.execute("BEGIN IMMEDIATE")

        cursor = connection.execute("""
            SELECT id
            FROM receipts
            WHERE filename = ?
              AND uploaded_by = ?
              AND claim_id IS NULL
        """, (receipt_filename, employee_id))

        receipt = cursor.fetchone()

        if receipt is None:
            connection.rollback()
            return None

        cursor = connection.execute("""
            INSERT INTO claims (
                employee_name,
                amount,
                category,
                description,
                receipt,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            employee_name,
            amount,
            category,
            description,
            receipt_filename,
            "Submitted"
        ))

        claim_id = cursor.lastrowid

        connection.execute("""
            UPDATE receipts
            SET claim_id = ?
            WHERE id = ?
              AND claim_id IS NULL
        """, (claim_id, receipt[0]))

        connection.commit()

        return claim_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
        
def update_claim_status(claim_id, status):
    connection = sqlite3.connect("reimbursement.db")
    connection.execute("""UPDATE claims 
    SET status = ?
    WHERE ID = ?""",( status, claim_id))
    connection.commit()
    connection.close()

def get_claims():
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("SELECT * FROM claims")
    claims = cursor.fetchall()
    connection.close()
    return claims

def delete_claim(claim_id):
    connection = sqlite3.connect("reimbursement.db")
    connection.execute("""DELETE FROM claims WHERE id =?""",
                       (claim_id,))
    connection.commit()
    connection.close()


def get_claims_by_employee(employee_name):
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("""
        SELECT * FROM claims
        WHERE employee_name = ?
    """, (employee_name,))
    claims = cursor.fetchall()
    connection.close()
    return claims


def get_claims_by_employee(employee_name):
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("""
        SELECT * FROM claims
        WHERE employee_name = ?
    """, (employee_name,))
    claims = cursor.fetchall()
    connection.close()
    return claims


def get_claims_by_employee(employee_name):
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("""
        SELECT * FROM claims
        WHERE employee_name = ?
    """, (employee_name,))
    claims = cursor.fetchall()
    connection.close()
    return claims


def get_claims_by_employee(employee_name):
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("""
        SELECT * FROM claims
        WHERE employee_name = ?
    """, (employee_name,))
    claims = cursor.fetchall()
    connection.close()
    return claims

def get_claims_by_employee(employee_name):
    connection = sqlite3.connect("reimbursement.db")
    cursor = connection.execute("""
        SELECT * FROM claims
        WHERE employee_name = ?
    """, (employee_name,))
    claims = cursor.fetchall()
    connection.close()
    return claims

def update_user_role(user_id, new_role):
    connection = sqlite3.connect("reimbursement.db")

    cursor = connection.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (new_role, user_id)
    )

    connection.commit()
    updated_rows = cursor.rowcount
    connection.close()

    return updated_rows

def get_categories():
    connection = sqlite3.connect("reimbursement.db")

    cursor = connection.execute("""
        SELECT id, category_name
        FROM categories
        ORDER BY category_name
    """)

    categories = cursor.fetchall()
    connection.close()

    return categories

def add_category(category_name):
    connection = sqlite3.connect("reimbursement.db")

    try:
        connection.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category_name,)
        )
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()

def set_category_limit(category_id, max_amount):
    connection = sqlite3.connect("reimbursement.db")

    try:
        cursor = connection.execute(
            "SELECT id FROM categories WHERE id = ?",
            (category_id,)
        )

        if cursor.fetchone() is None:
            return False

        connection.execute("""
            INSERT INTO category_limits (category_id, max_amount)
            VALUES (?, ?)
            ON CONFLICT(category_id)
            DO UPDATE SET max_amount = excluded.max_amount
        """, (category_id, max_amount))

        connection.commit()
        return True

    finally:
        connection.close()

def get_category_limit(category_name):
    connection = sqlite3.connect("reimbursement.db")

    cursor = connection.execute("""
        SELECT cl.max_amount
        FROM category_limits cl
        JOIN categories c
            ON cl.category_id = c.id
        WHERE c.category_name = ?
    """, (category_name,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    return result[0]

def add_payment_status_column():
    connection = sqlite3.connect("reimbursement.db")

    try:
        cursor = connection.execute("PRAGMA table_info(claims)")
        columns = [column[1] for column in cursor.fetchall()]

        if "payment_status" not in columns:
            connection.execute("""
                ALTER TABLE claims
                ADD COLUMN payment_status TEXT NOT NULL DEFAULT 'Pending'
            """)
            connection.commit()
            print("Payment status column added successfully.")
        else:
            print("Payment status column already exists.")

    finally:
        connection.close()

def get_approved_claims():
    connection = sqlite3.connect("reimbursement.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.execute("""
        SELECT
            id,
            employee_name,
            amount,
            category,
            description,
            status,
            payment_status
        FROM claims
        WHERE status = 'Approved'
        ORDER BY id DESC
    """)

    claims = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return claims

def update_payment_status(claim_id, payment_status):
    connection = sqlite3.connect("reimbursement.db")

    try:
        cursor = connection.execute("""
            UPDATE claims
            SET payment_status = ?
            WHERE id = ?
              AND status = 'Approved'
              AND payment_status = 'Pending'
        """, (payment_status, claim_id))

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()

def get_claim_summary():
    connection = sqlite3.connect("reimbursement.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.execute("""
        SELECT
            COUNT(*) AS total_claims,
            COALESCE(SUM(amount), 0) AS total_amount,
            COALESCE(SUM(
                CASE WHEN status = 'Approved' THEN 1 ELSE 0 END
            ), 0) AS approved_claims,
            COALESCE(SUM(
                CASE WHEN status = 'Submitted' THEN 1 ELSE 0 END
            ), 0) AS submitted_claims,
            COALESCE(SUM(
                CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END
            ), 0) AS rejected_claims,
            COALESCE(SUM(
                CASE WHEN status = 'Approved'
                  AND payment_status = 'Paid'
                THEN amount ELSE 0 END
            ), 0) AS paid_amount,
            COALESCE(SUM(
                CASE WHEN status = 'Approved'
                  AND payment_status = 'Pending'
                THEN amount ELSE 0 END
            ), 0) AS pending_payment_amount
        FROM claims
    """)

    summary = dict(cursor.fetchone())
    connection.close()

    return summary  

def get_category_summary():
    connection = sqlite3.connect("reimbursement.db")
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute("""
            SELECT
                category,
                COUNT(*) AS total_claims,
                COALESCE(SUM(amount), 0) AS total_amount
            FROM claims
            GROUP BY category
            ORDER BY category
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

def create_receipts_table():
    connection = sqlite3.connect("reimbursement.db")

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                uploaded_by INTEGER NOT NULL,
                claim_id INTEGER,
                FOREIGN KEY (uploaded_by) REFERENCES users(id),
                FOREIGN KEY (claim_id) REFERENCES claims(id)
            )
        """)

        connection.commit()

    finally:
        connection.close()

def save_receipt(filename, uploaded_by):
    connection = sqlite3.connect("reimbursement.db")

    try:
        connection.execute("""
            INSERT INTO receipts (filename, uploaded_by)
            VALUES (?, ?)
        """, (filename, uploaded_by))

        connection.commit()

    finally:
        connection.close()

def get_available_receipt(filename, employee_id):
    connection = sqlite3.connect("reimbursement.db")
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute("""
            SELECT id, filename, uploaded_by, claim_id
            FROM receipts
            WHERE filename = ?
              AND uploaded_by = ?
              AND claim_id IS NULL
        """, (filename, employee_id))

        receipt = cursor.fetchone()

        return dict(receipt) if receipt else None

    finally:
        connection.close()