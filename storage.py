import json
from pathlib import Path
from main import Alarm
from main import AlarmTypes

data_path = Path("alarms.json")

def save_alarms(alarms: list[Alarm]):
    data = []
    for alarm in alarms:
        data.append({
            "type": alarm.type.name,
            "threshold": alarm.threshold
        })

    with open(data_path, "w") as file:
        json.dump(data, file, indent=4)

def load_alarms():
    if not data_path.exists():
        return []

    alarms = []
    data = []

    with open(data_path, "r") as file:
        data = json.load(file)

    count = 0
    for i in data:
        alarms.append(Alarm(alarm_type=AlarmTypes[i["type"]], threshold=i["threshold"]))
        count += 1

    print(f"Loaded {count} alarms. ")

    return alarms
