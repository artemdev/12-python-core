from collections import UserDict
from datetime import date, datetime
import pickle

DEFAULT_DATE_FORMAT = '%m-%d-%Y'
DEFAULT_STORAGE_FILE_NAME = 'store.bin'


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.validate(value)

        self.__value = value

    def validate(self, value):
        raise NotImplementedError(
            f"Please define validation method in subclass {self.__class__.__name__}")


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
    def __init__(self):
        super().__init__()

        try:
            self.data = self.load_from_file()
        except FileNotFoundError:
            pass

    def add_record(self, record_instance):
        if (record_instance.get_name() in self.data):
            raise ValueError("Record already exists")

        self.data[record_instance.get_name()] = record_instance

        self.save_to_file()

        return self.data

    def find_by_name(self, name):
        if (name in self.data):
            return self.data[name]

    def find(self, term):
        found_records = set()

        for record in self.data.values():
            if (term in record.get_name()):
                found_records.add(record)

            for phone_number in record.get_phones():
                if term in phone_number:
                    found_records.add(record)

        return list(found_records)

    def delete(self, name):
        if self.find_by_name(name):
            del self.data[name]

    def iterator(self, n=1):
        values = list(self.data.values())

        for i in range(0, len(values)):
            yield values[i:i+n][0]

    def save_to_file(self):
        with open(DEFAULT_STORAGE_FILE_NAME, "wb") as fh:
            pickle.dump(self.data, fh)

    def load_from_file(self):
        unpacked = False

        with open(DEFAULT_STORAGE_FILE_NAME, "rb") as fh:
            unpacked = pickle.load(fh)

        return unpacked


# Створення нової адресної книги
book = AddressBook()

# # Створення запису для John
john_record = Record("11213", '12-1-1990')
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

results = book.find('1234')

for result in results:
    print(result)
