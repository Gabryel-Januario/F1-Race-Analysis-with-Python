import pandas as pd 
from ...config import RACES_CSV

def import_race_id():
    races = pd.read_csv(RACES_CSV)

    race = races[races['date'] == '2021-12-12']
    raceId = race['raceId'].values[0]
    return raceId
