import tkinter as tk
import time

class SystemMonitorUI:
    def __init__(self, root, metrics, db):
        self.root = root
        self.metrics = metrics
        self.db = db
        self.is_recording = False
        self.start_time = 0
        self.last_record_time = 0
        self.record_interval = 1  # Интервал по умолчанию
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Монитор системы")

        self.cpu_label = tk.Label(self.root, text="Загрузка ЦП: 0%")
        self.cpu_label.pack(pady=10)

        self.ram_label = tk.Label(self.root, text="ОЗУ: 0/0")
        self.ram_label.pack(pady=10)

        self.disk_label = tk.Label(self.root, text="ПЗУ: 0/0")
        self.disk_label.pack(pady=10)

        self.interval_label = tk.Label(self.root, text="Интервал (сек):")
        self.interval_label.pack(pady=10)

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack(pady=10)
        self.interval_entry.insert(0, "1")  # Установим значение по умолчанию

        self.set_interval_button = tk.Button(self.root, text="Установить интервал", command=self.set_interval)
        self.set_interval_button.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Начать запись", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Остановить", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.pack_forget()

        self.timer_label = tk.Label(self.root, text="Время записи: 00:00")
        self.timer_label.pack(pady=10)
        self.timer_label.pack_forget()

        self.update_metrics()

    def update_metrics(self):
        cpu_usage = self.metrics.get_cpu_usage()
        ram_free, ram_total = self.metrics.get_memory_usage()
        disk_free, disk_total = self.metrics.get_disk_usage()

        self.cpu_label.config(text=f"ЦП: {cpu_usage:.1f}%")
        self.ram_label.config(text=f"ОЗУ: свободно {ram_free:.1f} ГБ / всего {ram_total:.1f} ГБ")
        self.disk_label.config(text=f"ПЗУ: свободно {disk_free:.1f} ГБ / всего {disk_total:.1f} ГБ")

        if self.is_recording and (time.time() - self.last_record_time >= self.record_interval):
            self.db.insert_metrics(cpu_usage, ram_free, ram_total, disk_free, disk_total)
            self.last_record_time = time.time()

        self.root.after(1000, self.update_metrics)

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

    def set_interval(self):
        try:
            self.record_interval = int(self.interval_entry.get())
            if self.record_interval <= 0:
                raise ValueError("Интервал должен быть положительным числом.")
            print(f"Интервал обновления установлен на {self.record_interval} секунд.")
        except ValueError as e:
            print(f"Ошибка: {e}")