def confirm_return(title = ""):
    try:
        input(f"{title}Press <Enter> to continue. ")
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
        print("\nInvalid input.")

def select_multi_option(options: list, title = ""):
    while True:

        print()

        if title:
            print(title)

        for idx in range(len(options)):
            print(f"{idx+1}. {options[idx]}")

        try:
            selected_options_str = input("Select: ").split()
        except KeyboardInterrupt:
            return []

        selected_options_int = []

        is_invalid = False

        for idx in range(len(selected_options_str)):
            opt = selected_options_str[idx]
            try:
                opt = int(opt)
            except ValueError:
                confirm_return(f"Option \"{opt}\" is not a number. ")
                is_invalid = True
                break

            if 0 < opt <= len(options) and opt-1 not in selected_options_int:
                selected_options_int.append(opt-1)
            else:
                confirm_return(f"Number {opt} is not in range. ")
                is_invalid = True
                break

        if is_invalid:
            continue

        return selected_options_int

def select_action(actions, title = ""):
    # this function takes in a dictionary (actions). The keys are string which is the name of the option
    # that will be shown to the user and the value is a function which will run when the options is chosen. 

    print()

    if title:
        print(title)

    options = []
    idx = 0
    for opt in actions.keys():
        options.append(opt) # array of options so later it can pick the option based on idx

        print(f"{idx+1}. {opt}")

        idx += 1

    length = len(actions)
    selected_option_idx = select_int_range(f"Select option (1-{length}): ", 1, length) -1

    if selected_option_idx < 0: # if you pressed <Ctrl+c>
        return None

    selected_option = options[selected_option_idx]

    action = actions[selected_option]

    if action:
        return action   # the action will return true if it is supposed to exit the loop
                        # which is probably just the main loop
