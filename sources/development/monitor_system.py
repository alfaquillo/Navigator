import csv
import time
from datetime import datetime

CSV_FILE = "system_metrics.csv"
INTERVAL = 1.0


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return ""


def get_temp():
    raw = read_file("/sys/class/thermal/thermal_zone0/temp")
    try:
        return float(raw) / 1000.0
    except:
        return 0.0


def get_freq():
    paths = [
        "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq",
        "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq",
    ]

    for path in paths:
        raw = read_file(path)
        try:
            return float(raw) / 1000.0  # kHz -> MHz
        except:
            pass

    return 0.0


prev_total = 0
prev_idle = 0


def get_cpu_usage():
    global prev_total, prev_idle

    line = read_file("/proc/stat").splitlines()[0]
    values = [int(x) for x in line.split()[1:]]

    idle = values[3] + values[4]
    total = sum(values)

    diff_total = total - prev_total
    diff_idle = idle - prev_idle

    prev_total = total
    prev_idle = idle

    if diff_total == 0:
        return 0.0

    return 100.0 * (1.0 - diff_idle / diff_total)


with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "unix_time",
        "datetime",
        "cpu_usage_percent",
        "temperature_c",
        "cpu_freq_mhz"
    ])

    print("Monitoring started")

    try:
        while True:
            now = time.time()

            writer.writerow([
                now,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                round(get_cpu_usage(), 2),
                round(get_temp(), 2),
                round(get_freq(), 2)
            ])

            f.flush()

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("Monitoring stopped")
