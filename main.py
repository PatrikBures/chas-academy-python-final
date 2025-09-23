from simple_term_menu import TerminalMenu


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
    alarms = {
        "CPU": 0,
        "RAM": 0,
        "DISK": 0
    }
    def update_alarm(alarm):
        print(f"Current {alarm} alarm at {alarms[alarm]}%")
        new_alarm = select_int_range(f"New {alarm} alarm (0-100)%: ", 0, 100)

        if new_alarm == -1:
            return True

        confirmed = confirm(f"Updating alarm for {alarm} from {alarms[alarm]}% to {new_alarm}%, are you sure?")
        print()

        if confirmed:
            alarms[alarm] = new_alarm

    def cpu():
        update_alarm("CPU")
        return True

    def ram():
        update_alarm("RAM")
        return True

    def disk():
        update_alarm("DISK")
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
    print("show alarm")
def start_monitoring_mode():
    print("start mon mode")
def remove_alarm():
    print("remove alarm")
def _exit():
    return True

def main():
    actions = {
        "start monitoring": start_monitoring,
        "List active monitor": list_active_monitor,
        "Create alarm": create_alarm,
        "Show alarm": show_alarm,
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
