from prettytable import PrettyTable
import psutil

from time import sleep
from platform import system

import menu
import storage
from logger import *
from alarm_manager import AlarmManager



is_monitoring = False



def get_system_usage(am: AlarmManager):
    root_path = "/"

    if system() == "Windows":
        root_path = "C:\\"

    try:
        disk_usage = psutil.disk_usage(root_path)
    except FileNotFoundError:
        disk_usage = None

    return {
        am.AlarmTypes.CPU: psutil.cpu_percent(interval=1),
        am.AlarmTypes.RAM: psutil.virtual_memory(),
        am.AlarmTypes.DISK: disk_usage
    }

def bytes_to_gb(num):
    return round(num / 1024**3, 2)

def start_monitoring():
    global is_monitoring

    is_monitoring = True

    menu.confirm_return("Monitoring started. ")

def list_active_monitor(am: AlarmManager):
    if not is_monitoring:
        menu.confirm_return("Monitoring is not active. ")
        return
    
    usage = get_system_usage(am)

    table = PrettyTable()
    table.field_names = ["Type", "Usage %", "Usage", "Total"]
    table.align["Type"] = "l"
    table.align["Usage %"] = "r"
    table.align["Usage"] = "r"
    table.align["Total"] = "r"

    table.add_row(
        [
            "CPU",
            f"{usage[am.AlarmTypes.CPU]}%",
            "N/A",
            "N/A"
        ]
    )
    table.add_row(
        [
            "RAM",
            f"{usage[am.AlarmTypes.RAM].percent}%",
            f"{bytes_to_gb(usage[am.AlarmTypes.RAM].used)} GB",
            f"{bytes_to_gb(usage[am.AlarmTypes.RAM].total)} GB"
        ]
    )
    if usage[am.AlarmTypes.DISK] is not None:
        table.add_row(
            [
                "DISK",
                f"{usage[am.AlarmTypes.DISK].percent}%",
                f"{bytes_to_gb(usage[am.AlarmTypes.DISK].used)} GB",
                f"{bytes_to_gb(usage[am.AlarmTypes.DISK].total)} GB"
            ]
        )
    else:
        table.add_row(["DISK", "N/A", "N/A", "N/A"])

    print(table)

    menu.confirm_return()

def create_alarm(am: AlarmManager):
    def create_new_alarm(am: AlarmManager, new_alarm_type: AlarmManager.AlarmTypes):
        new_alarm_threshold = -2

        new_alarm_threshold = menu.select_int_range(f"Pick threshold for {new_alarm_type.name} alarm (1-100)%: ", 1, 100)

        if new_alarm_threshold < 1:
            return


        if am.alarm_exists(new_alarm_type, new_alarm_threshold):
            menu.confirm_return(f"{new_alarm_type.name} alarm with threshold {new_alarm_threshold}% already exists. ")
            return

        confirmed = menu.confirm(f"Creating new alarm for {new_alarm_type.name} with threshold {new_alarm_threshold}%, are you sure?")

        if confirmed:
            am.add_alarm(new_alarm_type, new_alarm_threshold)
            storage.save_alarms(am)
            log(f"{new_alarm_type.name}_{new_alarm_threshold}_alarm_created")


    def cpu():
        create_new_alarm(am, AlarmManager.AlarmTypes.CPU)

    def ram():
        create_new_alarm(am, AlarmManager.AlarmTypes.RAM)

    def disk():
        create_new_alarm(am, AlarmManager.AlarmTypes.DISK)

    def back():
        pass

    actions = {
        "CPU usage": lambda: cpu(),
        "Ram usage": lambda: ram(),
        "Disk usage": lambda: disk(),
        "Back": lambda: back()
    }

    menu.select_action(actions, "Select alarm type to configure")


def show_alarms(am: AlarmManager):
    if not am.has_alarms():
        menu.confirm_return("No alarms configured. ")
        return

    table = PrettyTable()
    table.field_names = ["Type", "Threshold"]
    table.align["Type"] = "l"
    table.align["Threshold"] = "r"

    for alarm in sorted(am.alarms, key=lambda x: (x.type, x.threshold)):
        table.add_row([alarm.type.name, f"{alarm.threshold}%"])

    print(table)

    menu.confirm_return()

def start_monitoring_mode(am: AlarmManager):
    if not am.has_alarms():
        menu.confirm_return("No alarms configured. ")
        return

    log("monitoring_mode_started")

    loop_max = 20
    loop_num = loop_max

    try: 
        while True:
            if loop_num >= loop_max:
                loop_num = 0
                print("Monitoring mode is active, press <Ctrl+c> to return to main menu.")
            loop_num += 1

            usage_current = get_system_usage(am)

            usage_current[am.AlarmTypes.RAM] = usage_current[am.AlarmTypes.RAM].percent

            if usage_current[am.AlarmTypes.DISK] is not None:
                usage_current[am.AlarmTypes.DISK] = usage_current[am.AlarmTypes.DISK].percent
            else:
                usage_current[am.AlarmTypes.DISK] = 0.0

            usage_warning = {
                am.AlarmTypes.CPU: 0.0,
                am.AlarmTypes.RAM: 0.0,
                am.AlarmTypes.DISK: 0.0
            }

            for alarm in am.alarms:
                # print(f"{type.name}, current: {usage_current[type]}%, alarm: {percentage}%, warning: {usage_warning[type]}%")
                if usage_current[alarm.type] > alarm.threshold and usage_current[alarm.type] > usage_warning[alarm.type]:
                    usage_warning[alarm.type] = alarm.threshold

            warned = False

            for type in usage_warning.keys():
                if usage_warning[type] <= 0.0:
                    continue

                print(f"*** WARNING, {type.name} USAGE IS ABOVE {usage_warning[type]}% ***")
                log(f"{type.name}_{usage_warning[type]}_alarm_activated")
                warned = True

            if warned:
                print()

            sleep(1)

    except KeyboardInterrupt:
        pass

    log("monitoring_mode_stopped")

def remove_alarm(am):
    if not am.has_alarms:
        menu.confirm_return("No alarms to remove. ")
        return

    options = []

    for alarm in am.alarms:
        options.append(f"{alarm.type.name} {alarm.threshold}%")

    indexes_to_delete = menu.select_multi_option(options, title="Pick alarms to delete: ")

    if not indexes_to_delete:
        return

    removed_alarms = 0

    indexes_to_delete.sort(reverse=True)

    for idx in indexes_to_delete:
        print(idx)
        log(f"{am.alarms[idx].type.name}_{am.alarms[idx].threshold}_alarm_deleted")
        am.remove_alarm(idx)
        removed_alarms += 1

    storage.save_alarms(am)

    menu.confirm_return(f"\nRemoved {removed_alarms} alarm/s. ")

def _exit():
    return True

def main():
    am = AlarmManager()
    storage.load_alarms(am)
    create_log_file()

    actions = {
        "Start monitoring":         lambda: start_monitoring(),
        "List active monitor":      lambda: list_active_monitor(am),
        "Create alarm":             lambda: create_alarm(am),
        "Show alarms":              lambda: show_alarms(am),
        "Start monitoring mode":    lambda: start_monitoring_mode(am),
        "Remove alarm":             lambda: remove_alarm(am),
        "Exit":                     lambda: _exit()
    }

    exit_loop = False
    while True:

        exit_loop = menu.select_action(actions)

        if exit_loop:
            break


if __name__ == "__main__":
    main()
