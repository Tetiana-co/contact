import pickle
import re
from pathlib import Path
from datetime import datetime

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self):
        name = input("Введіть ім'я: ")
        if not name:
            print("Ім'я не може бути порожнім!")
            return

        phones = []
        while True:
            phone = input("Введіть телефон (формат (123) 456-7890 або 1234567890) або натисніть Enter, щоб завершити: ")
            if phone == "":
                break
            if not self.is_valid_phone(phone):
                print("Некоректний формат телефону. Спробуйте ще раз.")
                continue
            phones.append(phone)

        email = input("Введіть email: ")
        if not self.is_valid_email(email):
            print("Некоректний формат email. Спробуйте ще раз.")
            return

        birthday = input("Введіть день народження (формат: ДД.ММ.РРРР): ")
        if not self.is_valid_birthday(birthday):
            print("Некоректний формат дня народження. Спробуйте ще раз.")
            return

        address = input("Введіть адресу: ")
        if not address:
            print("Адреса не може бути порожньою!")
            return

        self.contacts[name] = {
            "phones": phones,
            "email": email,
            "birthday": birthday,
            "address": address
        }
        print("Контакт додано!")

    def is_valid_phone(self, phone):
        phone_regex = r'^\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$'
        return bool(re.match(phone_regex, phone))

    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))

    def is_valid_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def delete_contact(self):
        name = input("Введіть ім'я для видалення: ")
        if name in self.contacts:
            del self.contacts[name]
            print(f"Контакт {name} видалено!")
        else:
            print(f"Контакт {name} не знайдено!")

    def show_contacts(self):
        if self.contacts:
            print("Список контактів:")
            for name, data in self.contacts.items():
                phones = ", ".join(data.get("phones", []))
                email = data.get("email", "")
                birthday = data.get("birthday", "")
                address = data.get("address", "")
                print(f"{name}: Телефон: {phones}, Email: {email}, День народження: {birthday}, Адреса: {address}")
        else:
            print("Адресна книга пуста.")

    def save_data(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        print("Дані успішно збережено!")

    @staticmethod
    def load_data(filename="addressbook.pkl"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                return pickle.load(f)
        else:
            print("Файл не знайдено. Створено нову адресу книгу.")
            return AddressBook()

    def search_contact(self):
        search_term = input("Введіть ім'я, email, адресу, день народження або номер телефону для пошуку: ").lower()
        found_contacts = []
        for name, data in self.contacts.items():
            if (
                search_term in name.lower()
                or search_term in data.get("email", "").lower()
                or search_term in data.get("address", "").lower()
                or search_term in data.get("birthday", "")
                or any(search_term in phone for phone in data.get("phones", []))
            ):
                found_contacts.append((name, data))

        if found_contacts:
            print("Знайдені контакти:")
            for name, data in found_contacts:
                phones = ", ".join(data.get("phones", []))
                email = data.get("email", "")
                birthday = data.get("birthday", "")
                address = data.get("address", "")
                print(f"{name}: Телефон: {phones}, Email: {email}, День народження: {birthday}, Адреса: {address}")
        else:
            print("Контакти не знайдено.")

    def edit_contact(self):
        name = input("Введіть ім'я контакту для редагування: ")
        if name in self.contacts:
            print(f"Редагуємо контакт {name}.")
            phones = self.contacts[name].get("phones", [])
            while True:
                phone = input("Введіть новий телефон (або Enter для завершення): ")
                if phone == "":
                    break
                if not self.is_valid_phone(phone):
                    print("Некоректний формат телефону. Спробуйте ще раз.")
                    continue
                phones.append(phone)

            email = input("Новий email (залиште порожнім для без змін): ")
            birthday = input("Новий день народження (залиште порожнім для без змін): ")
            address = input("Нова адреса (залиште порожнім для без змін): ")

            if email:
                if not self.is_valid_email(email):
                    print("Некоректний формат email.")
                    return
                self.contacts[name]["email"] = email
            if birthday:
                if not self.is_valid_birthday(birthday):
                    print("Некоректний формат дня народження.")
                    return
                self.contacts[name]["birthday"] = birthday
            if address:
                self.contacts[name]["address"] = address

            self.contacts[name]["phones"] = phones
            print(f"Контакт {name} оновлено!")
        else:
            print("Контакт не знайдено!")

def main():
    book = AddressBook.load_data()

    try:
        while True:
            print("\n1. Додати контакт")
            print("2. Видалити контакт")
            print("3. Показати всі контакти")
            print("4. Зберегти зміни")
            print("5. Пошук контакту")
            print("6. Редагувати контакт")
            print("7. Вийти")
            command = input("Виберіть опцію: ")

            if command == "1":
                book.add_contact()
            elif command == "2":
                book.delete_contact()
            elif command == "3":
                book.show_contacts()
            elif command == "4":
                book.save_data()
            elif command == "5":
                book.search_contact()
            elif command == "6":
                book.edit_contact()
            elif command == "7":
                break
            else:
                print("Невірний вибір, спробуйте ще раз.")
    finally:
        book.save_data()
        print("Дані успішно збережено!")

if __name__ == "__main__":
    main()
