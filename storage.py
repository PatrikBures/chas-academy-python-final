import json
from pathlib import Path
from main import Alarm

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
