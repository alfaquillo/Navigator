import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "system_metrics.csv"

df = pd.read_csv(CSV_FILE)

# Tiempo relativo
df["elapsed_s"] = df["unix_time"] - df["unix_time"].iloc[0]

fig, axs = plt.subplots(
    3,
    1,
    figsize=(14, 10),
    sharex=True
)

# ---------------------------------
# CPU usage
# ---------------------------------

axs[0].plot(
    df["elapsed_s"],
    df["cpu_usage_percent"]
)

axs[0].set_title("CPU Usage Over Time")
axs[0].set_ylabel("CPU (%)")
axs[0].grid(True)

# ---------------------------------
# Temperature
# ---------------------------------

axs[1].plot(
    df["elapsed_s"],
    df["temperature_c"]
)

axs[1].set_title("Temperature Over Time")
axs[1].set_ylabel("Temperature (°C)")
axs[1].grid(True)

# ---------------------------------
# CPU frequency
# ---------------------------------

axs[2].plot(
    df["elapsed_s"],
    df["cpu_freq_mhz"]
)

axs[2].set_title("CPU Frequency Over Time")
axs[2].set_ylabel("Frequency (MHz)")
axs[2].set_xlabel("Time (s)")
axs[2].grid(True)

plt.tight_layout()

plt.savefig(
    "system_overview.png",
    dpi=200
)

plt.show()
