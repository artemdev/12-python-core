from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if value:
            return value

        raise ValueError("Name should be present!")


class Phone(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if (value.isdigit() and len(value) == 10):
            return value

        raise ValueError("Name must contain only letters")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def get_name(self):
        return self.name.value

    def get_phones(self):
        return [phone.value for phone in self.phones]

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in self.get_phones():
            raise ValueError("Phone not found")

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for saved_phone in self.phones:
            if (saved_phone.value == phone):
                return saved_phone

    def remove_phone(self, phone):
        for saved_phone in self.phones:
            if (saved_phone.value == phone):

                self.phones.remove(saved_phone)
                break


class AddressBook(UserDict):
    def add_record(self, record_instance):
        if (self.find(record_instance.get_name())):
            raise ValueError("Record already exists")

        self.data[record_instance.get_name()] = record_instance

        return self.data

    def find(self, name):
        if (name in self.data):

            return self.data[name]

    def delete(self, name):
        if self.find(name):
            del self.data[name]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
