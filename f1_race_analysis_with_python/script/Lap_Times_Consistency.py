import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .utils.Import_Race_Id import import_race_id

def lap_times_consistency(lap_times, drivers):
    race_id = import_race_id()

    lap_times['seconds'] = lap_times['milliseconds'] / 1000
    lap_times_Abu_Dhabi_GP_2021 = lap_times[lap_times['raceId'] == race_id]

    consistency_by_driver = lap_times_Abu_Dhabi_GP_2021.groupby('driverId')['seconds'].agg(['mean', 'std']).round(2).reset_index()
    consistency_by_driver = consistency_by_driver.sort_values(by='std')

    consistency_by_driver = consistency_by_driver.merge(drivers[['driverId', 'driverRef']], on='driverId')
    consistency_by_driver = consistency_by_driver[['driverId', 'driverRef', 'mean', 'std']]
    consistency_by_driver['driverRef'] = consistency_by_driver['driverRef'].str.upper()

    plt.figure(figsize=(12, 6))

    sns.barplot(data=consistency_by_driver, x='driverRef', y='std', order=consistency_by_driver.sort_values('std')['driverRef'])

    plt.xticks(rotation=45, ha='right')
    plt.title('Driver Consistency (Standard Deviation of Lap Times)')
    plt.xlabel('Drivers')
    plt.ylabel('Standard Deviation (s)')
    plt.tight_layout()
    plt.show()