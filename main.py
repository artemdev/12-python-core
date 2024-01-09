from collections import UserDict
from datetime import date, datetime

DEFAULT_DATE_FORMAT = '%m-%d-%Y'


class Field:
    def __init__(self, value):
        if self.validate(value):
            self.__value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def set(self, value):
        validated_value = self.validate(value)

        if validated_value:
            self.__value = validated_value

    def validate(self, value):
        raise AttributeError(
            f'Please define validate method in {self.__class__.__name__} class', )


class Name(Field):
    def validate(self, value):
        if value.strip():
            return value

        raise ValueError("Name should be present!")


class Phone(Field):
    def validate(self, value):
        if (value.isdigit() and len(value) == 10):
            return value

        raise ValueError("Phone must contain at least 10 digits")


class Birthday(Field):
    def validate(self, value):
        if not value or datetime.strptime(value, DEFAULT_DATE_FORMAT):
            return value


class Record:
    def __init__(self, name, birthday=''):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
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

    def days_to_birthday(self):
        if not self.birthday.value:
            return None

        birthday_date = datetime.strptime(
            self.birthday.value, DEFAULT_DATE_FORMAT).date()

        this_year_birthday = birthday_date.replace(year=date.today().year)

        if this_year_birthday < date.today():
            this_year_birthday = this_year_birthday.replace(
                year=this_year_birthday.year + 1)

        days_until_birthday = (this_year_birthday - date.today()).days

        if days_until_birthday == 0:
            return 'Happy Birthday!'
        else:
            return days_until_birthday


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

    def iterator(self, n=1):
        values = list(self.data.values())

        for i in range(0, len(values)):
            yield values[i:i+n][0]


# Створення нової адресної книги
book = AddressBook()

# # Створення запису для John
john_record = Record("John1", '12-1-1990')
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
print(john_record)
print(john_record.days_to_birthday())
book.add_record(john_record)

book_iterator = book.iterator(1)

for i in book_iterator:
    print(i)


# john_record2 = Record("John3", '01-09-1190')
# john_record2.add_phone("1234567890")
# john_record2.add_phone("5555555555")

# john_record3 = Record("John1", '01-09-1190')
# john_record3.add_phone("1234567890")
# john_record3.add_phone("5555555555")

# book.add_record(john_record2)
# book.add_record(john_record3)


# # print(next(iterator))
# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane", '09-01-1990')
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")


# # Виведення: Contact name: John, phones: 1112223333; 5555555555
# print('days to birthday', john.days_to_birthday())

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# book.delete("Jane")
