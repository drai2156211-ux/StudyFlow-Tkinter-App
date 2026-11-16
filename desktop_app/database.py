
import sqlite3
import hashlib
import os
import hmac
from pathlib import Path


class StudyFlowDatabase:

    def __init__(self):

        self.folder = Path(__file__).parent / "database"
        self.folder.mkdir(exist_ok=True)

        self.db_path = self.folder / "studyflow.db"

        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):

        connection = self.connect()
        cursor = connection.cursor()

        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                deadline TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    # ==================================
    # PASSWORD SECURITY
    # ==================================

    def hash_password(self, password, salt=None):

        if salt is None:
            salt = os.urandom(16).hex()

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            200000
        ).hex()

        return password_hash, salt

    # ==================================
    # REGISTER USER
    # ==================================

    def register_user(self, username, password):

        password_hash, salt = self.hash_password(password)

        connection = self.connect()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO users
                (username, password_hash, salt)
                VALUES (?, ?, ?)
            """, (username, password_hash, salt))

            connection.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            connection.close()

    # ==================================
    # LOGIN USER
    # ==================================

    def verify_user(self, username, password):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT password_hash, salt
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()
        connection.close()

        if user is None:
            return False

        stored_hash, salt = user

        entered_hash, _ = self.hash_password(
            password,
            salt
        )

        return hmac.compare_digest(
            stored_hash,
            entered_hash
        )

    # ==================================
    # ADD TASK
    # ==================================

    def add_task(self, title, subject, deadline, priority):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks
            (title, subject, deadline, priority, status)
            VALUES (?, ?, ?, ?, 'Pending')
        """, (title, subject, deadline, priority))

        connection.commit()
        connection.close()

    # ==================================
    # GET TASKS
    # ==================================

    def get_tasks(self):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT task_id, title, subject,
                   deadline, priority, status
            FROM tasks
            ORDER BY task_id DESC
        """)

        tasks = cursor.fetchall()
        connection.close()

        return tasks

    # ==================================
    # UPDATE TASK
    # ==================================

    def update_task(
        self, task_id, title, subject, deadline, priority
    ):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?,
                subject = ?,
                deadline = ?,
                priority = ?
            WHERE task_id = ?
        """, (title, subject, deadline, priority, task_id))

        connection.commit()
        connection.close()

    def complete_task(self, task_id):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = 'Completed'
            WHERE task_id = ?
        """, (task_id,))

        connection.commit()
        connection.close()

    # ==================================
    # DELETE TASK
    # ==================================

    def delete_task(self, task_id):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE task_id = ?
        """, (task_id,))

        connection.commit()
        connection.close()

    # ==================================
    # DASHBOARD STATISTICS
    # ==================================

    def get_statistics(self):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM tasks
            WHERE status = 'Pending'
        """)
        pending = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM tasks
            WHERE status = 'Completed'
        """)
        completed = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT subject)
            FROM tasks
        """)
        subjects = cursor.fetchone()[0]

        connection.close()

        return total, pending, completed, subjects


if __name__ == "__main__":

    db = StudyFlowDatabase()

    print("StudyFlow database connected!")
    print("Tasks:", db.get_tasks())
    print("Statistics:", db.get_statistics())
    print("Users table ready!")
