from prettytable import PrettyTable
import psutil

from enum import Enum
from time import sleep
from platform import system

import menu
import storage


class AlarmTypes(Enum):
    CPU = 0
    RAM = 1
    DISK = 2

class Alarm:
    def __init__(self, alarm_type, threshold):
        self.type = alarm_type
        self.threshold = threshold

alarms = []
is_monitoring = False


def get_usage():
    root_path = "/"

    if system() == "Windows":
        root_path = "C:\\"

    try:
        disk_usage = psutil.disk_usage(root_path)
    except FileNotFoundError:
        disk_usage = None

    return {
        AlarmTypes.CPU: psutil.cpu_percent(interval=1),
        AlarmTypes.RAM: psutil.virtual_memory(),
        AlarmTypes.DISK: disk_usage
    }

def bytes_to_gb(num):
    return round(num / 1024 / 1024 / 1024, 2)

def start_monitoring():
    global is_monitoring

    is_monitoring = True

    menu.confirm_return("Monitoring started. ")

def list_active_monitor():
    if not is_monitoring:
        menu.confirm_return("Monitoring is not active. ")
        return
    
    usage = get_usage()

    table = PrettyTable()
    table.field_names = ["Type", "Usage %", "Usage", "Total"]
    table.align["Type"] = "l"
    table.align["Usage %"] = "r"
    table.align["Usage"] = "r"
    table.align["Total"] = "r"

    table.add_row(
        [
            "CPU",
            f"{usage[AlarmTypes.CPU]}%",
            "N/A",
            "N/A"
        ]
    )
    table.add_row(
        [
            "RAM",
            f"{usage[AlarmTypes.RAM].percent}%",
            f"{bytes_to_gb(usage[AlarmTypes.RAM].used)} GB",
            f"{bytes_to_gb(usage[AlarmTypes.RAM].total)} GB"
        ]
    )
    if usage[AlarmTypes.DISK] is not None:
        table.add_row(
            [
                "DISK",
                f"{usage[AlarmTypes.DISK].percent}%",
                f"{bytes_to_gb(usage[AlarmTypes.DISK].used)} GB",
                f"{bytes_to_gb(usage[AlarmTypes.DISK].total)} GB"
            ]
        )
    else:
        table.add_row(["DISK", "N/A", "N/A", "N/A"])

    print(table)

    menu.confirm_return()

def create_alarm():
    def create_new_alarm(new_alarm_type: AlarmTypes):
        new_alarm_threshold = -2

        new_alarm_threshold = menu.select_int_range(f"Pick threshold for {new_alarm_type.name} alarm (1-100)%: ", 1, 100)

        if new_alarm_threshold < 1:
            return True


        for alarm in alarms:
            if alarm.type == new_alarm_type and alarm.threshold == new_alarm_threshold:
                menu.confirm_return(f"{new_alarm_type.name} alarm with threshold {new_alarm_threshold}% already exists. ")
                return

        confirmed = menu.confirm(f"Creating new alarm for {new_alarm_type.name} with threshold {new_alarm_threshold}%, are you sure?")

        if confirmed:
            new_alarm = Alarm(new_alarm_type, new_alarm_threshold)
            alarms.append(new_alarm)
            storage.save_alarms(alarms)


    def cpu():
        create_new_alarm(AlarmTypes.CPU)
        return True

    def ram():
        create_new_alarm(AlarmTypes.RAM)
        return True

    def disk():
        create_new_alarm(AlarmTypes.DISK)
        return True

    def back():
        return True

    actions = {
        "CPU usage": cpu,
        "Ram usage": ram,
        "Disk usage": disk,
        "Back": back
    }

    menu.select_action(actions, "Select alarm type to configure")

def show_alarm():
    if not alarms:
        menu.confirm_return("No alarms configured. ")
        return

    table = PrettyTable()
    table.field_names = ["Type", "Threshold"]
    table.align["Type"] = "l"
    table.align["Threshold"] = "r"

    for alarm in sorted(alarms, key=lambda x: x.threshold):
        table.add_row([alarm.type.name, f"{alarm.threshold}%"])

    print(table)

    menu.confirm_return()

def start_monitoring_mode():
    if not alarms:
        menu.confirm_return("No alarms configured. ")
        return

    loop_max = 20
    loop_num = loop_max

    while True:
        if loop_num >= loop_max:
            loop_num = 0
            print("Monitoring mode is active, press <Ctrl+c> to return to main menu.")
        loop_num += 1

        try:
            usage_current = get_usage()

            usage_current[AlarmTypes.RAM] = usage_current[AlarmTypes.RAM].percent

            if usage_current[AlarmTypes.DISK] is not None:
                usage_current[AlarmTypes.DISK] = usage_current[AlarmTypes.DISK].percent
            else:
                usage_current[AlarmTypes.DISK] = 0.0

            usage_warning = {
                AlarmTypes.CPU: 0.0,
                AlarmTypes.RAM: 0.0,
                AlarmTypes.DISK: 0.0
            }

            for alarm in alarms:
                # print(f"{type.name}, current: {usage_current[type]}%, alarm: {percentage}%, warning: {usage_warning[type]}%")
                if usage_current[alarm.type] >= alarm.threshold and usage_current[alarm.type] > usage_warning[alarm.type]:
                    usage_warning[alarm.type] = alarm.threshold

            warned = False

            for type in usage_warning.keys():
                if usage_warning[type] <= 0.0:
                    continue

                print(f"*** WARNING, {type.name} USAGE IS ABOVE OR {usage_warning[type]}% ***")
                warned = True

            if warned:
                print()

            sleep(1)

        except KeyboardInterrupt:
            break

def remove_alarm():
    if not alarms:
        menu.confirm_return("No alarms to remove. ")
        return

    options = []

    for alarm in alarms:
        options.append(f"{alarm.type.name} {alarm.threshold}%")

    indexes_to_delete = menu.select_multi_option(options, title="Pick alarms to delete: ")

    if not indexes_to_delete:
        return

    removed_alarms = 0

    for idx in reversed(indexes_to_delete):
        alarms.pop(idx)
        removed_alarms += 1

    menu.confirm_return(f"\nRemoved {removed_alarms} alarm/s. ")

def _exit():
    return True

def main():
    global alarms
    alarms = storage.load_alarms()

    actions = {
        "Start monitoring": start_monitoring,
        "List active monitor": list_active_monitor,
        "Create alarm": create_alarm,
        "Show alarms": show_alarm,
        "Start monitoring mode": start_monitoring_mode,
        "Remove alarm": remove_alarm,
        "Exit": _exit
    }

    while True:
        exit_loop = menu.select_action(actions)

        if exit_loop:
            break


if __name__ == "__main__":
    main()
