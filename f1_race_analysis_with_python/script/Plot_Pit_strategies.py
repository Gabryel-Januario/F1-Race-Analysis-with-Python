
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from .utils.Import_Race_Id import import_race_id
race_id = import_race_id()

def detect_pit_strategies(lap_times, pit_stops, drivers, race_id=race_id, laps_after_stop=2):
    lap_times = lap_times[lap_times['raceId'] == race_id]
    pit_stops = pit_stops[pit_stops['raceId'] == race_id]
    
    lap_times = lap_times.merge(drivers[['driverId', 'code']], on='driverId')
    pit_stops = pit_stops.merge(drivers[['driverId', 'code']], on='driverId')
    lap_times['position'] = pd.to_numeric(lap_times['position'], errors='coerce')

    strategy_results = []

    pit_stops = pit_stops.sort_values('lap')

    for _, pit1 in pit_stops.iterrows():
        driver1 = pit1['code']
        pit_lap1 = pit1['lap']
        
        
        pos_before1 = lap_times[(lap_times['code'] == driver1) & (lap_times['lap'] == pit_lap1 - 1)]
        if pos_before1.empty:
            continue
        pos1 = int(pos_before1['position'].values[0])

        for _, pit2 in pit_stops.iterrows():
            driver2 = pit2['code']
            pit_lap2 = pit2['lap']

            if driver1 == driver2:
                continue

            if abs(pit_lap1 - pit_lap2) > 3:
                continue

            pos_before2 = lap_times[(lap_times['code'] == driver2) & (lap_times['lap'] == pit_lap2 - 1)]
            if pos_before2.empty:
                continue
            pos2 = int(pos_before2['position'].values[0])

            if abs(pos1 - pos2) > 2:
                continue

            first_pit = driver1 if pit_lap1 < pit_lap2 else driver2
            second_pit = driver2 if first_pit == driver1 else driver1
            first_pit_lap = min(pit_lap1, pit_lap2)
            second_pit_lap = max(pit_lap1, pit_lap2)

            analysis_lap = second_pit_lap + laps_after_stop

            pos_first = lap_times[(lap_times['code'] == first_pit) & (lap_times['lap'] == analysis_lap)]
            pos_second = lap_times[(lap_times['code'] == second_pit) & (lap_times['lap'] == analysis_lap)]

            if pos_first.empty or pos_second.empty:
                continue

            pos_first = int(pos_first['position'].values[0])
            pos_second = int(pos_second['position'].values[0])

            if pos_first < pos_second:
                strategy = 'undercut'
            elif pos_first > pos_second:
                strategy = 'overcut'
            else:
                strategy = 'no effect'

            strategy_results.append({
                'driver_1': driver1,
                'driver_2': driver2,
                'pitted_first': first_pit,
                'pitted_after': second_pit,
                'first_pit_lap': first_pit_lap,
                'second_pit_lap': second_pit_lap,
                'pos_first_after': pos_first,
                'pos_second_after': pos_second,
                'strategy': strategy
            })

    pit_strategies = pd.DataFrame(strategy_results)

    plt.figure(figsize=(10, 6))
    sns.countplot(data=pit_strategies, x='strategy', palette='Set2', hue='strategy')
    plt.title("Number of undercuts and overcuts ", fontsize=16)
    plt.xlabel("Strategy", fontsize=12)
    plt.ylabel("Number of cases", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
