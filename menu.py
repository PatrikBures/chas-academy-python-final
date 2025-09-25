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

    for action in actions.keys():
        options.append(action)

    while True:
        print()

        if title:
            print(title)

        idx = 0
        for opt in options:
            print(f"{idx+1}. {opt}")

            idx += 1

        selected_option_idx = select_int_range(f"Select option (1-{len(options)}): ", 1, len(options)) -1

        if selected_option_idx < 0: # if you pressed <Ctrl+c>
            return True

        selected_option = options[selected_option_idx]

        action = actions[selected_option]

        if action:
            exit_loop = action()

            if exit_loop:
                return True
