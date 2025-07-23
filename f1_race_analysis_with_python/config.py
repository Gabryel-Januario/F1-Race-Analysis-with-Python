from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / 'data'
RACES_CSV = DATA_DIR / 'races.csv'
lAP_TIMES_CSV = DATA_DIR / 'lap_times.csv'
DRIVERS_CSV = DATA_DIR / 'drivers.csv'
PIT_STOPS_CSV = DATA_DIR / 'pit_stops.csv'
RESULTS_CSV = DATA_DIR / 'results.csv'
CONSTRUCTORS_CSV = DATA_DIR / 'constructors.csv'
