from datetime import datetime
from pathlib import Path
from os import mkdir

dir_path=Path("logs")
log_path=Path(f"{dir_path}/{datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}.csv")

def log(string_to_log):
    with open(log_path, "a") as file:
        date = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        file.write(f"\n{date},{string_to_log}")

def create_log_file():
    if log_path.exists():
        return

    if not dir_path.exists():
        mkdir(dir_path)

    with open(log_path, "w") as file:
        file.write("Date,Time,Entry")
