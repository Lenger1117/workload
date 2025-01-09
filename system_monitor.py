import psutil
import tkinter as tk
import sqlite3
import time

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Монитор системы")
        
        self.cpu_label = tk.Label(root, text="Загрузка ЦП: 0%")
        self.cpu_label.pack(pady=10)

        self.ram_label = tk.Label(root, text="ОЗУ: 0/0")
        self.ram_label.pack(pady=10)

        self.disk_label = tk.Label(root, text="ПЗУ: 0/0")
        self.disk_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Начать запись", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Остановить", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.pack_forget()

        self.timer_label = tk.Label(root, text="Время записи: 00:00")
        self.timer_label.pack(pady=10)
        self.timer_label.pack_forget()

        self.is_recording = False
        self.start_time = 0

        self.create_database()
        self.update_metrics()
    
    def create_database(self):
        self.conn = sqlite3.connect('system_monitor.db')
        self.cursor = self.conn.cursor()
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

    def update_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        ram_total = ram.total / (1024 ** 3)
        ram_free = ram.free / (1024 ** 3)

        disk_total = disk.total / (1024 ** 3)
        disk_free = disk.free / (1024 ** 3)

        self.cpu_label.config(text=f"ЦП: {cpu_usage}%")
        self.ram_label.config(text=f"ОЗУ: свободно {ram_free:.2f} ГБ / всего {ram_total:.2f} ГБ")
        self.disk_label.config(text=f"ПЗУ: свободно {disk_free:.2f} ГБ / всего {disk_total:.2f} ГБ")

        if self.is_recording:
            self.record_metrics(cpu_usage, ram_free, ram_total, disk_free, disk_total)

        self.root.after(1000, self.update_metrics)

    def record_metrics(self, cpu_usage, ram_free, ram_total, disk_free, disk_total):
        self.cursor.execute('''
            INSERT INTO system_metrics (cpu_usage, ram_free, ram_total, disk_free, disk_total)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpu_usage, ram_free, ram_total, disk_free, disk_total))
        self.conn.commit()

    def start_recording(self):
        self.is_recording = True
        self.start_time = time.time()
        self.start_button.pack_forget()
        self.stop_button.pack(pady=10)
        self.timer_label.pack(pady=10)
        self.update_timer()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.pack(pady=10)
        self.stop_button.pack_forget()
        self.timer_label.pack_forget()

    def update_timer(self):
        if self.is_recording:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.config(text=f"Время записи: {minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()