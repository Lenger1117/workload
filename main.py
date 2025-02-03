import tkinter as tk
import tkinter as tk
from db import Database
from system_monitor import Metrics
from ui import SystemMonitorUI

if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    metrics = Metrics()
    app = SystemMonitorUI(root, metrics, db)
    root.protocol("WM_DELETE_WINDOW", lambda: (db.close(), root.destroy()))
    root.mainloop()