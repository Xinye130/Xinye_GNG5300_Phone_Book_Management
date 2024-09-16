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
    
    def is_valid_email(self, email):
        if email == "":
            return True
        
        # Regular expression for validating an email address: (user_name)@(domain_name).(top-leveldomain)  
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email) is not None
    
    def is_valid_phone_number(self, phone_number):
        # Regular expression for validating a phone number: (###) ###-####
        phone_number_regex = re.compile(r'\(\d{3}\) \d{3}-\d{4}')
        return re.fullmatch(phone_number_regex, phone_number) is not None
    
    def input_mandatory_field(self, value):
        while value == "":
            value = input("Mandatory field. Please enter a valid value: ").strip()
        return value
 
    def create_contact(self):
        while True:
            print("How would you like to add contacts:")
            print("1. Add contact manually")
            print("2. Import contacts from CSV")
            print("Or enter -1 to exit.")
            choice = input("Enter your choice (1/2/-1): ")

            if choice == '1':
                first_name = self.input_mandatory_field(input("Enter first name: ").strip())
                last_name = self.input_mandatory_field(input("Enter last name: ").strip())
                phone_number = self.input_mandatory_field(input("Enter phone number in the format (###) ###-####: ").strip())
                while not self.is_valid_phone_number(phone_number):
                    phone_number = input("Invalid phone number. Please try again: ").strip()
                email_address = input("Enter email address (or press Enter to skip): ").strip()
                while not self.is_valid_email(email_address):
                    email_address = input("Invalid email address. Please try again: ").strip()
                address = input("Enter address (or press Enter to skip): ").strip()

                new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                self.contacts.append(new_contact)
                print(f"Contact added: {first_name} {last_name}, {phone_number}, {email_address}, {address}\n")

            elif choice == '2':
                # add validate phone number, email, and madatory fields
                # only add qualified contacts, output error, output succeeded number
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

            elif choice == '-1':
                print("Exiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def search_contact(self):
        while True:
            print("Do you want to search by:")
            print("1. Full name")
            print("2. Telephone number")
            print("Or enter -1 to exit.")
            search_type = input("Enter your choice (1/2/-1): ").strip()

            if search_type in ['1', '2']:
                search_query = self.input_mandatory_field(input("Enter the search query: ").strip()) 
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
            
            elif search_type == '-1':
                print("Exiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def update_contact(self):
        while True:
            search_query = self.input_mandatory_field(input("Enter the name of the contact to be updated (or -1 to exit): ").strip())

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

            field_index = 'invalid'
            while not field_index == '-1':
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
                    break

                new_value = input("Enter the new value: ").strip()
                if (field_index in ['1', '2', '3']):
                    new_value = self.input_mandatory_field(new_value)
                if (field_index == '3'):
                    while not self.is_valid_phone_number(new_value):
                        new_value = input("Phone number must be in format (###) ###-###. Please try again: ").strip()
                if (field_index == '4'):
                    while not self.is_valid_email(new_value):
                        new_value = input("Invalid email address. Please try again (or press Enter to delete previous email address): ").strip()
                print('\n')

                # if possible add confirm whether to update
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
    
    def delete_contact(self):
        while True:
            print("How would you like to delete contacts:")
            print("1. Delete manually")
            print("2. Batch delete from CSV")
            print("Or enter -1 to exit.")
            choice = input("Enter your choice (1/2/-1): ").strip()

            if choice == '-1':
                print("Exiting.\n")
                break

            elif choice == '1':
                delete_query = self.input_mandatory_field(input("Enter the name of the contact to delete: ").strip())

                matches = []
                for contact in self.contacts:
                    query_name = ''.join(delete_query.lower().split())
                    full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                    if query_name in full_name:
                        matches.append(contact)

                if not matches:
                    print(f"Contact '{delete_query}' not found.\n")
                else:
                    self.print_contact_list(matches)

                    if len(matches) > 1:
                        index = -2
                        while index < -1 or index >= len(matches):
                            try:
                                index = int(input("Enter the index of the contact to delete (or -1 to exit): ").strip())
                                if index < -1 or index >= len(matches):
                                    print("Invalid index. Please try again.")
                            except ValueError:
                                print("Invalid index. Please try again.")
                        if index == -1:
                            print('\n')
                            continue
                        contact_to_delete = matches[index]
                    else:
                        choice = ''
                        while choice not in ['-1', '1']:
                            choice = input("Do you want to delete this contact? Enter 1 to delete or -1 to exit: ").strip().lower()
                        if choice == '-1':
                            print('\n')
                            continue
                        contact_to_delete = matches[0]
                    
                    delete_name = f"{contact_to_delete.get_first_name()} {contact_to_delete.get_last_name()}"
                    self.contacts.remove(contact_to_delete)
                    print(f"Contact deleted: {delete_name}\n")

            elif choice == '2':
                csv_file = input("Enter the path to the CSV file: ").strip()
                try:
                    with open(csv_file, newline='') as file:
                        reader = csv.reader(file)
                        attempted_deletions = 0
                        successful_deletions = 0
                        for row in reader:
                            if row:
                                full_name = row[0].strip()
                                if full_name:
                                    attempted_deletions += 1
                                    found = False
                                    for contact in self.contacts:
                                        contact_full_name = f"{contact.get_first_name()} {contact.get_last_name()}"
                                        if contact_full_name == full_name:
                                            self.contacts.remove(contact)
                                            print(f"[Succeeded] Contact deleted: {contact_full_name}")
                                            successful_deletions += 1
                                            found = True
                                            break
                                    if not found:
                                        print(f"[Failed] Contact '{full_name}' not found.")
                        print(f"Batch delete completed: {successful_deletions}/{attempted_deletions} contacts deleted successfully.\n")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")

            else:
                print("Invalid choice. Please try again.\n")

phone_book = PhoneBook()
phone_book.create_contact()
phone_book.print_all_contacts()
#phone_book.search_contact()
#phone_book.update_contact()
phone_book.delete_contact()
phone_book.print_all_contacts()