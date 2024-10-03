import os
import platform
import time

def get_uptime():
    if platform.system() == "Windows":
        from subprocess import check_output
        output = check_output("net stats workstation", shell=True).decode()
        for line in output.splitlines():
            if "Statistics since" in line:
                boot_time_str = line.split("Statistics since")[1].strip()
                boot_time = time.strptime(boot_time_str, '%d/%m/%Y %H:%M:%S')
                boot_timestamp = time.mktime(boot_time)
                uptime_seconds = time.time() - boot_timestamp
                return uptime_seconds

    elif platform.system() == "Linux" or platform.system() == "Darwin":
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds

    else:
        raise NotImplementedError("Unsupported OS")

def format_uptime(seconds):
    days = int(seconds // (24 * 3600))
    seconds = seconds % (24 * 3600)
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{days} days, {hours} hours, {minutes} minutes, {int(seconds)} seconds"
