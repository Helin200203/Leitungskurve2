import pandas as pd
import json

def read_my_csv(file_path="activity.csv"):
    column_names = ["HeartRate", "Duration", "PowerOriginal"]
    df = pd.read_csv(file_path, sep=",", header=0, usecols=column_names)
    df["Duration"] = df.index
    return df


def calculate_zones(max_heart_rate, heart_rate_data, power_data):
    zones = {
        'Zone 1': (0, 0.5 * max_heart_rate),
        'Zone 2': (0.5 * max_heart_rate, 0.6 * max_heart_rate),
        'Zone 3': (0.6 * max_heart_rate, 0.7 * max_heart_rate),
        'Zone 4': (0.7 * max_heart_rate, 0.8 * max_heart_rate),
        'Zone 5': (0.8 * max_heart_rate, max_heart_rate)
    }
    zone_times = {zone: 0 for zone in zones}
    zone_power = {zone: [] for zone in zones}

    for hr, power in zip(heart_rate_data, power_data):
        for zone, (lower, upper) in zones.items():
            if lower <= hr < upper:
                zone_times[zone] += 1
                zone_power[zone].append(power)

    avg_power = {zone: (sum(powers)/len(powers)) if powers else 0 for zone, powers in zone_power.items()}
    
    return zone_times, avg_power

