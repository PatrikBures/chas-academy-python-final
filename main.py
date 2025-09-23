from simple_term_menu import TerminalMenu
from prettytable import PrettyTable
from enum import Enum
from time import sleep
import psutil


class AlarmTypes(Enum):
    CPU = 0
    RAM = 1
    DISK = 2

alarms_percentage = []
alarms_type = []


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
        new_alarm_value = -2

        new_alarm_value = select_int_range(f"New {alarm_type.name} alarm (1-100)%: ", 1, 100)

        if new_alarm_value < 1:
            return True

        confirmed = confirm(f"Creating new alarm for {alarm_type.name} at {new_alarm_value}%, are you sure?")
        print()

        if confirmed:
            alarms_percentage.append(new_alarm_value)
            alarms_type.append(alarm_type)

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

    for type, percentage in sorted(zip(alarms_type, alarms_percentage), key=lambda x: x[1]):
        table.add_row([type.name, f"{percentage}%"])

    print(table)

    input("Press enter to go back to main menu.")

def start_monitoring_mode():
    if not alarms_type:
        print("No alarms configured.")
        return


    loop = 1000
    while True:
        if loop >= 20:
            loop = 0
            print("Monitoring mode is active, press Ctrl+C to return to main menu.")
        loop += 1

        try:
            usage_current = get_usage()
            usage_warning = {
                AlarmTypes.CPU: 0.0,
                AlarmTypes.RAM: 0.0,
                AlarmTypes.DISK: 0.0
            }

            for type, percentage in zip(alarms_type, alarms_percentage):
                # print(f"{type.name}, current: {usage_current[type]}%, alarm: {percentage}%, warning: {usage_warning[type]}%")
                if usage_current[type] >= percentage and usage_current[type] > usage_warning[type]:
                    usage_warning[type] = percentage

            for type in usage_warning.keys():
                if usage_warning[type] <= 0.0:
                    continue
                print(f"*** WARNING, {type.name} USAGE IS ABOVE/AT {usage_warning[type]}% ***")

            sleep(1)

        except KeyboardInterrupt:
            break


def remove_alarm():
    if not alarms_percentage:
        print("No alarms to remove")
        return

    options = []

    for idx in range(len(alarms_percentage)):
        options.append(f"{alarms_type[idx].name} {alarms_percentage[idx]}%")
    
    terminal_menu = TerminalMenu(options, title="Pick alarms to delete: ", multi_select=True)

    indexes_to_delete = terminal_menu.show()

    removed_alarms = 0

    if type(indexes_to_delete) == tuple:
        for idx in indexes_to_delete:
            alarms_percentage.pop(idx)
            alarms_type.pop(idx)
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
