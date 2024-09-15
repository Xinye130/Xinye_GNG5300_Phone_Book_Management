from contact import Contact
from tabulate import tabulate
import csv
import re

#contact = contact.Contact("John", "Doe", "555-555-5555", "", "")

#print(contact.get_update_time())

class PhoneBook:
    def __init__(self):
        self.contacts = []

    def print_contacts(self):
        if not self.contacts:
            print("No contacts available.\n")
            return

        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()] for contact in self.contacts]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

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

    def find_contact(self):
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
                    headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
                    rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                            contact.get_email_address(), contact.get_address()] for contact in matches]
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                    print("\n")
                else:
                    print("No contact meets the requirement.\n")
            
            elif search_type == '3':
                print("Exiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")


phone_book = PhoneBook()
phone_book.create_contact()
phone_book.print_contacts()
phone_book.find_contact()