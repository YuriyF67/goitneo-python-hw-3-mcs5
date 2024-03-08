from collections import UserDict, defaultdict
from datetime import datetime, timedelta


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me proper parameters, please."
        except KeyError:
            return "Give me proper parameters, please."
        except IndexError:
            return "Give me proper parameters, please."

    return wrapper


class Field:
    def __init__(self, value):
        self.value = value

    @input_error
    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, number):
        if len(number) == 10 and number.isdigit():
            super().__init__(number)
        else:
            print("Invalid phone number format, must be 10 digits")


class Birthday(Field):
    def __init__(self, birthday):
        try:
            self.date = datetime.strptime(birthday, "%d.%m.%Y").date()
            super().__init__(str(self.date))
        except ValueError:
            print("Invalid birthday format (DD.MM.YYYY)")


class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
            else:
                print(f"Phone number: {phone_number} not found.")

    def edit_phone(self, phone_number, new_number):
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_number
                return
            print(f"Phone number: {phone_number} not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
            print(f"Phone number: {phone_number} not found.")

    def show_birthday(self):
        if self.birthday:
            return f"birthday: {self.birthday.date.strftime('%d.%m.%Y')}"
        else:
            return "birthday: Not available."

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, {self.show_birthday()}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def birthdays_this_week(self):
        birthdays_by_weekday = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            name = record.name.value
            birthday = record.birthday.date if record.birthday else None

            if birthday:
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days < 7:
                    birthday_weekday = (today + timedelta(days=delta_days)).strftime(
                        "%A"
                    )
                    birthdays_by_weekday[birthday_weekday].append(name)

        result = ""
        for weekday, names in birthdays_by_weekday.items():
            if weekday != "Sunday":
                result += f"{weekday}: {', '.join(names)}\n"
            else:
                result += f"{'Monday'}: {', '.join(names)}\n"
        return result


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    existing_record = book.find(name)

    if existing_record:
        existing_record.add_phone(phone)
        return f"Phone added for existing contact {name}."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "New contact added."


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return f"Contact {name} not found."


@input_error
def show_birthday(args, book):
    (name,) = args
    record = book.find(name)
    if record:
        return record.show_birthday()
    else:
        print(f"Contact {name} not found.")


@input_error
def change_phone(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Phone number for {name} updated to {new_phone}."
    else:
        print(f"Contact {name} not found.")


@input_error
def get_phone(args, book):
    (name,) = args
    record = book.find(name)
    if record:
        phones = [str(phone) for phone in record.phones]
        return f"Phone numbers for {name}: {', '.join(phones)}"
    else:
        print(f"Contact {name} not found.")


@input_error
def get_all_contacts(book):
    if not book:
        return "Address Book is empty."

    contact_list = []
    for record in book.values():
        contact_list.append(str(record))

    return "\n".join(contact_list)


def main():
    book = AddressBook()

    print(f"Welcome to the assistant bot!\n\nEnter 'hello' to get started.\n")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print(
                f"How can I help you?\n\nAvailable commands:\n add [Name] [phone_number 10 digits],\n change [Name] [phone_number 10 digits],\n phone [Name],\n all (prints whole Address Book),\n add-birthday [Name] [birthday DD.MM.YYYY],\n show-birthday [Name],\n birthdays (showing birthdays for coming week),\n close (exiting bot),\n exit (exiting bot)"
            )
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "birthdays":
            print(book.birthdays_this_week())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
