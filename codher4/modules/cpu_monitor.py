import psutil

def get_cpu_usage_by_process():
    process_data = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = proc.info['cpu_percent']
            if cpu > 0.5:  # Filter small CPU consumers
                process_data.append({
                    "name": proc.info['name'],
                    "cpu": cpu
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(process_data, key=lambda x: x["cpu"], reverse=True)[:15]
