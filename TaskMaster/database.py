import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "tasks.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create tasks table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            priority TEXT,
            due_date TEXT,
            created_at TEXT,
            completed BOOLEAN DEFAULT 0
        )
        ''')
        
        # Create categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT
        )
        ''')
        
        self.conn.commit()

    def add_task(self, title: str, description: str = "", category: str = None,
                 priority: str = "Medium", due_date: str = None) -> int:
        cursor = self.conn.cursor()
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
        INSERT INTO tasks (title, description, category, priority, due_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, category, priority, due_date, created_at))
        
        self.conn.commit()
        return cursor.lastrowid

    def get_all_tasks(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def update_task(self, task_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
            
        cursor = self.conn.cursor()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs.keys())
        query = f"UPDATE tasks SET {set_clause} WHERE id = ?"
        
        cursor.execute(query, list(kwargs.values()) + [task_id])
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_category(self, name: str, color: str = "#000000") -> int:
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)',
                         (name, color))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return -1

    def get_all_categories(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM categories')
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def __del__(self):
        self.conn.close() 