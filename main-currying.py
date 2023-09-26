from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join([str(record) for record in self.data.values()])

    def iterator(self, page_size):
        def address_generator():
            current_page = 0
            while current_page < len(self.data):
                yield list(self.data.values())[current_page:current_page + page_size]
                current_page += page_size

        return address_generator()


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validate(self):
        pass

    def set_value(self, value):
        self.value = value
        self.validate()


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def validate(self):
        if not (len(self.value) == 10 and self.value.isdigit()):
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def validate(self):
        try:
            datetime.strptime(self.value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Invalid birthday format (DD-MM-YYYY)")

    def as_datetime(self):
        return datetime.strptime(self.value, '%d-%m-%Y')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, number):
        phone = Phone(number)
        self.phones.append(phone)

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        if old_number in [phone.value for phone in self.phones]:
            self.remove_phone(old_number)
            self.add_phone(new_number)
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone

    def days_to_birthday(self, birthday_date=None):
        if self.birthday:
            today = datetime.now()
            self.birthday.as_datetime()

            next_birthday = birthday_date.replace(year=today.year)
            if today > next_birthday:
                next_birthday = birthday_date.replace(year=today.year + 1)

            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        return f"Name: {self.name.value}, Phones: {[phone.value for phone in self.phones]}, Birthday: {self.birthday.value if self.birthday else 'Not specified'}"


def main():
    address_book = AddressBook()

    def add_func(args):
        _, name, phone, *birthday = args
        birthday = birthday[0] if birthday else None
        record = Record(name, birthday)
        record.add_phone(phone)
        address_book.add_record(record)
        print(f"Record for {name} added to the address book.")

    def del_func(args):
        _, name = args
        address_book.delete(name)
        print(f"Record for {name} deleted from the address book.")

    def find_func(args):
        _, name = args
        record = address_book.find(name)
        if record:
            print(f"Found record: {record}")
        else:
            print(f"No record found for {name}.")

    def edit_func(args):
        _, name, new_phone = args
        record = address_book.find(name)
        if record:
            record.phones = [Phone(new_phone)]
            print(f"Phone number for {name} edited to {new_phone}.")
        else:
            print(f"No record found for {name}.")

    def show_func(args):
        print(address_book)

    def birthday_func(args):
        _, name = command.split(' ', 1)
        record = address_book.find(name)
        if record:
            days_left = record.days_to_birthday()
            if days_left is not None:
                print(f"Days left to {name}'s birthday: {days_left} days")
            else:
                print(f"{name} has no birthday specified.")
        else:
            print(f"No record found for {name}.")

    COMMANDS = {
        'add ': add_func,
        'delete ': del_func,
        'find ': find_func,
        'edit ': edit_func,
        'show all': show_func,
        'birthday ': birthday_func
    }

    while True:
        command = input("Enter a command: ").strip().lower()
        parts = command.split(' ')

        if command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif parts[0] in COMMANDS:
            func = COMMANDS[parts[0]]
            func(parts[1:])
        else:
            print("Invalid command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
