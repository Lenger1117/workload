import psutil

class Metrics:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent()

    @staticmethod
    def get_memory_usage():
        ram = psutil.virtual_memory()
        return ram.free / (1024 ** 3), ram.total / (1024 ** 3)

    @staticmethod
    def get_disk_usage():
        disk = psutil.disk_usage('/')
        return disk.free / (1024 ** 3), disk.total / (1024 ** 3)