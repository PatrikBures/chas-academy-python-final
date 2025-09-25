from datetime import datetime
from pathlib import Path

log_path=Path("log.csv")

def log(string_to_log):
    with open(log_path, "a") as file:
        dt = datetime.now()
        file.write(f"\n{dt.year}-{dt.month}-{dt.day}\t{dt.hour}:{dt.minute}:{dt.second}\t{string_to_log}")

def create_log_file():
    if log_path.exists():
        return

    with open(log_path, "w") as file:
        file.write("Date\tTime\tEntry")
