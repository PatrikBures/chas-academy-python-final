from simple_term_menu import TerminalMenu

def confirm_return(title = ""):
    try:
        input(f"{title}Press <Enter> to return. ")
    except KeyboardInterrupt:
        pass

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
