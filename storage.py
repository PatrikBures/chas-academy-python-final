import json
from pathlib import Path
from alarm_manager import AlarmManager, AlarmTypes

data_path = Path("alarms.json")

def save_alarms(am: AlarmManager):
    data = []
    # converts list with alarms to list with dictionaries so it can be saved to a json file
    for alarm in am.alarms:
        data.append({
            "type": alarm.type.name,
            "threshold": alarm.threshold
        })

    with open(data_path, "w") as file:
        json.dump(data, file, indent=4)

def load_alarms(am: AlarmManager):
    if not data_path.exists():
        return

    data = []

    with open(data_path, "r") as file:
        data = json.load(file)

    count = 0
    # converts list of dictionaries to a list of alarms
    for i in data:
        am.add_alarm(AlarmTypes[i["type"]], i["threshold"])
        count += 1

    print(f"Loaded {count} alarms. ")

