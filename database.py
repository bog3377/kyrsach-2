import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='schedule.db'):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS examiners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER,
                    examiner_id INTEGER,
                    room_id INTEGER,
                    datetime TEXT NOT NULL,
                    duration_hours INTEGER NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups (id),
                    FOREIGN KEY (examiner_id) REFERENCES examiners (id),
                    FOREIGN KEY (room_id) REFERENCES rooms (id)
                )
            ''')
            conn.commit()

    def add_group(self, name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO groups (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    def add_examiner(self, name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO examiners (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    def add_room(self, name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO rooms (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    def add_exam(self, name, group_id, examiner_id, room_id, datetime_str, duration_hours, duration_minutes):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exams (name, group_id, examiner_id, room_id, datetime, duration_hours, duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, group_id, examiner_id, room_id, datetime_str, duration_hours, duration_minutes))
            conn.commit()
            return cursor.lastrowid

    def get_groups(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM groups ORDER BY name')
            return cursor.fetchall()

    def get_examiners(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM examiners ORDER BY name')
            return cursor.fetchall()

    def get_rooms(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM rooms ORDER BY name')
            return cursor.fetchall()

    def get_exams(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.id, e.name, g.name, ex.name, r.name, e.datetime, e.duration_hours, e.duration_minutes
                FROM exams e
                JOIN groups g ON e.group_id = g.id
                JOIN examiners ex ON e.examiner_id = ex.id
                JOIN rooms r ON e.room_id = r.id
                ORDER BY e.datetime
            ''')
            return cursor.fetchall()

    def update_exam(self, exam_id, name, group_id, examiner_id, room_id, datetime_str, duration_hours, duration_minutes):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE exams 
                SET name=?, group_id=?, examiner_id=?, room_id=?, datetime=?, duration_hours=?, duration_minutes=?
                WHERE id=?
            ''', (name, group_id, examiner_id, room_id, datetime_str, duration_hours, duration_minutes, exam_id))
            conn.commit()

    def delete_exam(self, exam_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM exams WHERE id=?', (exam_id,))
            conn.commit()