def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_phone(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return f"Phone number for {name} updated to {new_phone}."
    else:
        return f"Contact {name} not found."


def get_phone(args, contacts):
    (name,) = args
    if name in contacts:
        return f"Phone number for {name}: {contacts[name]}"
    else:
        return f"Contact {name} not found."


def get_all_contacts(contacts):
    phone_book = "Phone Book:\n"
    for name, phone in contacts.items():
        phone_book += f"{name}: {phone}\n"
    return phone_book


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_phone(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(get_all_contacts(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
