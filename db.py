import sqlite3

class Database:
    def __init__(self, db_name='system_monitor.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_usage REAL,
                ram_free REAL,
                ram_total REAL,
                disk_free REAL,
                disk_total REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_metrics(self, cpu_usage, ram_free, ram_total, disk_free, disk_total):
        self.cursor.execute('''
            INSERT INTO system_metrics (cpu_usage, ram_free, ram_total, disk_free, disk_total)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpu_usage, ram_free, ram_total, disk_free, disk_total))
        self.conn.commit()

    def close(self):
        self.conn.close()