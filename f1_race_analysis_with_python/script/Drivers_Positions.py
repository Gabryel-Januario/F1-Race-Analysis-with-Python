
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np

from ..config.constants import lAP_TIMES_CSV, DRIVERS_CSV
from .utils.Import_Race_Id import import_race_id

def plot_drivers_positions(drivers_code):
    lap_times = pd.read_csv(lAP_TIMES_CSV)
    drivers = pd.read_csv(DRIVERS_CSV)
    race_id = import_race_id()

    laps = lap_times[lap_times["raceId"] == race_id]
    laps = laps.merge(drivers[["driverId", "code"]], on="driverId")
    laps = laps[["raceId", "driverId", "code", "lap", "position"]]
    
    laps_per_driver = laps[laps["code"].isin(drivers_code)]

    plt.figure(figsize=(14, 6))

    sns.set_theme(style="whitegrid")

    for driver in drivers_code:
        data_drive = laps_per_driver[laps_per_driver["code"] == driver]

        sns.lineplot(data=data_drive,
                x="lap", 
                y="position", 
                marker="o", 
                linewidth=2.5,
                label=driver
                )


    plt.title("Positions per driver", fontsize=16, fontweight='bold')
    plt.xlabel("Lap", fontsize=12)
    plt.ylabel("Position",  fontsize=12)
    plt.legend(title='Drivers')

    plt.gca().invert_yaxis() 

    xticks = np.arange(0, 59, 2)
    xticks = np.append(xticks, 58) 
    plt.xticks(xticks)

    plt.yticks(fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()
