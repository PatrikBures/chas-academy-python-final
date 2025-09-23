from simple_term_menu import TerminalMenu
from prettytable import PrettyTable
from enum import Enum
from time import sleep
import psutil


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

    usage = {
        AlarmTypes.CPU: -1.0,
        AlarmTypes.RAM: -1.0,
        AlarmTypes.DISK: -1.0
    }
    
    usage[AlarmTypes.CPU] = psutil.cpu_percent(interval=1)
    usage[AlarmTypes.RAM] = psutil.virtual_memory().percent
    usage[AlarmTypes.DISK] = psutil.disk_usage('/').percent
    
    return usage
def select_int_range(title, min, max):
    while True:
        num = ""
        try:
            num = input(title)
        except KeyboardInterrupt:
            return -1

        try:
            num = int(num)
        except ValueError:
            print("Not a number!\n")
            continue
        if min <= num <= max:
            return num
        else:
            print(f"Number not in range ({min}-{max})\n")

def confirm(question):
    while True:
        ans = ""

        try:
            ans = input(f"{question} (Y/n): ")
        except KeyboardInterrupt:
            return False
        
        match ans.lower():
            case "" | "y":
                return True
            case "n":
                return False


def select_action(actions, title = ""):
    options = []
    for opt in actions.keys():
        options.append(opt)

    terminal_menu = TerminalMenu(options, title=title)

    while True:
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) == int:
            selected_option = options[menu_entry_index]
            action = actions[selected_option]

            if action:
                exit_loop = action()

                if exit_loop:
                    return True
        else: 
            return True


def start_monitoring():
    print("start monitoring")

def list_active_monitor():
    print("list")

def create_alarm():
    def create_new_alarm(alarm_type: AlarmTypes):
        new_alarm_threshold = -2

        new_alarm_threshold = select_int_range(f"New {alarm_type.name} alarm (1-100)%: ", 1, 100)

        if new_alarm_threshold < 1:
            return True

        confirmed = confirm(f"Creating new alarm for {alarm_type.name} with threshold {new_alarm_threshold}%, are you sure?")
        print()

        if confirmed:
            alarm = Alarm(alarm_type, new_alarm_threshold)
            alarms.append(alarm)

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

    select_action(actions, "Select alarm to configure")


def show_alarm():
    table = PrettyTable()
    table.field_names = ["Alarm type", "Alarm %"]
    table.align["Alarm type"] = "l"
    table.align["Alarm %"] = "r"

    for alarm in sorted(alarms, key=lambda x: x.threshold):
        table.add_row([alarm.type.name, f"{alarm.threshold}%"])

    print(table)

    input("Press enter to go back to main menu.")

def start_monitoring_mode():
    if not alarms:
        print("No alarms configured.")
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
            usage_warning = {
                AlarmTypes.CPU: 0.0,
                AlarmTypes.RAM: 0.0,
                AlarmTypes.DISK: 0.0
            }

            for alarm in alarms:
                # print(f"{type.name}, current: {usage_current[type]}%, alarm: {percentage}%, warning: {usage_warning[type]}%")
                if usage_current[alarm.type] >= alarm.threshold and usage_current[alarm.type] > usage_warning[alarm.type]:
                    usage_warning[alarm.type] = alarm.threshold

            for type in usage_warning.keys():
                if usage_warning[type] <= 0.0:
                    continue
                print(f"*** WARNING, {type.name} USAGE IS ABOVE/AT {usage_warning[type]}% ***")

            sleep(1)

        except KeyboardInterrupt:
            break


def remove_alarm():
    if not alarms:
        print("No alarms to remove")
        return

    options = []

    for alarm in alarms:
        options.append(f"{alarm.type.name} {alarm.threshold}%")
    
    terminal_menu = TerminalMenu(options, title="Pick alarms with <Space> to delete: ", multi_select=True)

    indexes_to_delete = terminal_menu.show()

    removed_alarms = 0

    if type(indexes_to_delete) == tuple:
        for idx in indexes_to_delete:
            alarms.pop(idx)
            removed_alarms += 1

    print(f"Removed {removed_alarms} alarm/s")


def _exit():
    return True

def main():
    actions = {
        "start monitoring": start_monitoring,
        "List active monitor": list_active_monitor,
        "Create alarm": create_alarm,
        "Show alarms": show_alarm,
        "Start monitoring mode": start_monitoring_mode,
        "Remove alarm": remove_alarm,
        "Exit": _exit
    }


    while True:
        exit_loop = select_action(actions)

        if exit_loop:
            break


if __name__ == "__main__":
    main()
