from contact import Contact
from tabulate import tabulate
import csv
import re

#contact = contact.Contact("John", "Doe", "555-555-5555", "", "")

#print(contact.get_update_time())

class PhoneBook:
    def __init__(self):
        self.contacts = []

    def print_all_contacts(self):
        if not self.contacts:
            print("No contacts available.\n")
            return

        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()] for contact in self.contacts]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n")
    
    def print_contact(self, contact):
        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()]]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n")

    def print_contact_list(self, contacts):
        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()] for contact in contacts]
        print(tabulate(rows, headers=headers, tablefmt="grid", showindex="always"))

    def create_contact(self):
        while True:
            print("Select an option:")
            print("1. Add contact manually")
            print("2. Import contacts from CSV")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                # add forcing name input
                # add check and parse phone number format
                # add check for email format
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                phone_number = input("Enter phone number: ")
                email_address = input("Enter email address (optional): ") or ""
                address = input("Enter address (optional): ") or ""

                new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                self.contacts.append(new_contact)
                print(f"Contact added: {first_name} {last_name}, {phone_number}, {email_address}, {address}\n")

            elif choice == '2':
                csv_file = input("Enter the path to the CSV file: ")
                try:
                    with open(csv_file, newline='') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if len(row) >= 3:
                                first_name, last_name, phone_number = row[:3]
                                email_address = row[3] if len(row) > 3 else ""
                                address = row[4] if len(row) > 4 else ""
                                new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                                self.contacts.append(new_contact)
                                print(f"Contact added: {first_name} {last_name}, {phone_number}, {email_address}, {address}")
                        print("Contacts imported successfully from CSV.\n")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")

            elif choice == '3':
                print("Exiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def search_contact(self):
        while True:
            print("Do you want to search by:")
            print("1. Full name")
            print("2. Telephone number")
            print("Or enter 3 to exit.")
            search_type = input("Enter your choice (1/2/3): ").strip()

            if search_type in ['1', '2']:
                search_query = input("Enter the search query: ")
                matches = []

                for contact in self.contacts:
                    if search_type == '1':
                        query_name = ''.join(search_query.lower().split())
                        full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                        if query_name in full_name:
                            matches.append(contact)
                    elif search_type == '2':
                        query_number = re.sub(r'\D', '', search_query)
                        phone_number = re.sub(r'\D', '', contact.get_phone_number())
                        if query_number in phone_number:
                            matches.append(contact)

                if matches:
                    print("Here are the contacts that meet the requirement:")
                    self.print_contact_list(matches)
                    print("\n")
                else:
                    print("No contact meets the requirement.\n")
            
            elif search_type == '3':
                print("Exiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def update_contact(self):
        while True:
            search_query = input("Enter the name of the contact to be updated (or -1 to exit): ").strip()

            if search_query == '-1':
                print('\n')
                break

            matches = []
            for contact in self.contacts:
                query_name = ''.join(search_query.lower().split())
                full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                if query_name in full_name:
                    matches.append(contact)

            if not matches:
                print("No contact matches the query. Please try again.")
                continue

            self.print_contact_list(matches)

            if len(matches) > 1:
                index = -2
                while index < -1 or index >= len(matches):
                    try:
                        index = int(input("Enter the index of the contact to update (or -1 to exit): ").strip())
                        if index < -1 or index >= len(matches):
                            print("Invalid index. Please try again.")
                    except ValueError:
                        print("Invalid index. Please try again.")
                if index == -1:
                    print('\n')
                    continue
                contact_to_update = matches[index]
            else:
                choice = ''
                while choice not in ['-1', '1']:
                    choice = input("Do you want to update this contact? Enter 1 to update or -1 to exit: ").strip().lower()
                if choice == '-1':
                    print('\n')
                    continue
                contact_to_update = matches[0]

            print("\nThe contact to update is:")
            self.print_contact(contact_to_update)

            print("Which field do you want to update?")
            print("1. First Name")
            print("2. Last Name")
            print("3. Phone Number")
            print("4. Email Address")
            print("5. Address")
            field_index = input("Enter the index of the field to update (or -1 to exit): ").strip()

            while field_index not in ['-1', '1', '2', '3', '4', '5']:
                field_index = input("Invalid index. Please try again: ").strip()

            if field_index == '-1':
                print('\n')
                continue

            new_value = input("Enter the new value: ").strip()
            print('\n')

            if field_index == '1':
                contact_to_update.set_first_name(new_value)
            elif field_index == '2':
                contact_to_update.set_last_name(new_value)
            elif field_index == '3':
                contact_to_update.set_phone_number(new_value)
            elif field_index == '4':
                contact_to_update.set_email_address(new_value)
            elif field_index == '5':
                contact_to_update.set_address(new_value)

            print("The contact is now: ")
            self.print_contact(contact_to_update)

phone_book = PhoneBook()
phone_book.create_contact()
phone_book.print_all_contacts()
#phone_book.search_contact()
phone_book.update_contact()