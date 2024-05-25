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

def load_person_data(file_path="data/person_db.json"):
    """Eine Funktion, die weiß, wo die Personendatenbank ist, und ein Wörterbuch mit den Personen zurückgibt."""
    with open(file_path, "r") as file:
        person_data = json.load(file)
    return person_data

def get_person_list(file_path="data/person_db.json"):
    """Eine Funktion, die eine Liste von Personen zurückgibt."""
    person_data = load_person_data(file_path)
    return [f"{person['lastname']}, {person['firstname']}" for person in person_data]

def find_person_data_by_name(suchstring, file_path="data/person_db.json"):
    """Eine Funktion, der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurückgibt."""
    person_data = load_person_data(file_path)
    
    if suchstring == "None":
        return {}

    try:
        lastname, firstname = suchstring.split(", ")
    except ValueError:
        return {}

    for person in person_data:
        if person["lastname"] == lastname and person["firstname"] == firstname:
            return person

    return {}
