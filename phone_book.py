from contact import Contact
from tabulate import tabulate
import csv
import json
import re
from collections import defaultdict
from datetime import datetime

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
        print()
    
    def print_contact(self, contact):
        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()]]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print()

    def print_contact_list(self, contacts, show_index=True, show_create_time=False, show_update_time=False):
        headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
        if show_create_time:
            headers.append("Create Time")
            rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address(), contact.get_create_time()] for contact in contacts]
            print(tabulate(rows, headers=headers, tablefmt="grid", showindex = show_index))
            return
        
        if show_update_time:
            headers.append("Update Time")
            rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address(), contact.get_update_time()] for contact in contacts]
            print(tabulate(rows, headers=headers, tablefmt="grid", showindex = show_index))
            return
        
        rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                 contact.get_email_address(), contact.get_address()] for contact in contacts]
        print(tabulate(rows, headers=headers, tablefmt="grid", showindex = show_index))
    
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
    
    def is_contact_exist(self, first_name, last_name):
        full_name_to_check = f"{first_name.lower()} {last_name.lower()}"
        for contact in self.contacts:
            full_name = f"{contact.get_first_name().lower()} {contact.get_last_name().lower()}"
            if full_name == full_name_to_check:
                return True
        return False

    def input_mandatory_field(self, value):
        while value == "":
            value = input("Mandatory field. Please enter a valid value: ").strip()
        return value
 
    def create_contact(self):
        while True:
            print("How would you like to add contacts:")
            print("1. Add contact manually")
            print("2. Import contacts from CSV")
            print("Or enter q to quit.")
            choice = input("Enter your choice (1/2/q): ")

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

                if not self.is_contact_exist(first_name, last_name):
                    new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                    self.contacts.append(new_contact)
                    print(f"Contact added: {first_name} {last_name}, {phone_number}, {email_address}, {address}\n")
                else:
                    print(f"Failed to add contact. Contact '{first_name} {last_name}' already exists.\n")
                    continue

            elif choice == '2':
                csv_file = input("Enter the path to the CSV file: ")
                try:
                    with open(csv_file, newline='') as file:
                        reader = csv.reader(file)
                        attempted_additions = 0
                        successful_additions = 0
                        for row in reader:
                            attempted_additions += 1
                            first_name = row[0].strip() if row else ""
                            last_name = row[1].strip() if len(row) > 1 else ""
                            phone_number = row[2].strip() if len(row) > 2 else ""
                            email_address = row[3] if len(row) > 3 else ""
                            address = row[4] if len(row) > 4 else ""

                            is_valid = True
                            error_message = f"[Failed] Contact {attempted_additions} not added: "

                            # Check for duplicated contacts
                            if self.is_contact_exist(first_name, last_name):
                                is_valid = False
                                error_message += f"Contact '{first_name} {last_name}' already exists. "
                            
                            # Check for mandatory fields, validate phone number and email
                            if not first_name:
                                is_valid = False
                                error_message += "First name missing. "
                            if not last_name: 
                                is_valid = False
                                error_message += "Last name missing. "
                            if not phone_number:
                                is_valid = False
                                error_message += "Phone number missing. "
                            if phone_number and not self.is_valid_phone_number(phone_number):
                                is_valid = False
                                error_message += "Phone number invalid, should be in format (###) ###-####. "
                            if email_address and not self.is_valid_email(email_address):
                                is_valid = False
                                error_message += "Email address invalid. "                           
                            
                            if is_valid:
                                successful_additions += 1
                                new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                                self.contacts.append(new_contact)
                                print(f"[Succeeded] Contact {attempted_additions} added: {first_name} {last_name}, {phone_number}, {email_address}, {address}")
                            else:
                                print(error_message)
                        print(f"Batch addition completed: {successful_additions}/{attempted_additions} contacts added successfully.\n")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")

            elif choice == 'q':
                print("Quiting.\n")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def search_contact(self):
        while True:
            print("Search contacts by:")
            print("1. Full name")
            print("2. Telephone number")
            print("3. Date created")
            print("Or enter q to quit.")
            search_type = input("Enter your choice (1/2/3/q): ").strip()

            while search_type not in ['1', '2', '3', 'q']:
                search_type = input("Invalid choice. Please enter a valid option: ").strip()
            
            if search_type == 'q':
                print("Quiting.\n")
                break

            matches = []
            show_create_time = False
            if search_type in ['1', '2']:
                search_query = self.input_mandatory_field(input("Enter the search query: ").strip()) 

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
            
            elif search_type == '3':
                matches = self.search_contacts_by_date()
                show_create_time = True

            if matches:
                print("\nHere are the contacts that meet the requirement:")
                self.print_contact_list(matches, True, show_create_time)
            else:
                print("No contact meets the requirement.\n")
                continue

            index = -2
            while index < -1 or index >= len(matches):
                try:
                    index = int(input("View history of changes by entering contact index (or -1 to quit): ").strip())
                    if index < -1 or index >= len(matches):
                        print("Invalid index. Please try again.\n")
                except ValueError:
                    print("Invalid index. Please try again.\n")
            if index == -1:
                print("Quiting.\n")
                continue
            contact_to_view = matches[index]

            print("\nHistory of changes:")
            contact_to_view.print_history()
            print()

    def search_contacts_by_date(self):
        print("\nSearch contacts by date (inclusively):")
        print("Enter a single date (yyyy-mm-dd) or a date range (yyyy-mm-dd yyyy-mm-dd)")
        print("Or enter 'q' to quit.")
        dates = input("Enter: ").strip().split()

        matches = []
        is_valid_date = False
        while not is_valid_date:
            if len(dates) == 1:
                if dates[0] == 'q':
                    print("Quiting.\n")
                    return matches
                
                try:
                    start_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
                    end_date = start_date
                    is_valid_date = True
                except ValueError:
                    dates = input("Invalid date format. Please try again: ").strip().split()
            
            elif len(dates) == 2:
                try:
                    start_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
                    end_date = datetime.strptime(dates[1], '%Y-%m-%d').date()
                    is_valid_date = True
                except ValueError:
                    dates = input("Invalid date format. Please try again: ").strip().split()
            
            else:
                dates = input("Invalid date format. Please try again: ").strip().split()

        for contact in self.contacts:
            create_time = contact.get_create_time().date()
            if start_date <= create_time <= end_date:
                matches.append(contact)
        
        return matches

    def update_contact(self):
        while True:
            print("Update contact")
            search_query = self.input_mandatory_field(input("Enter the name of the contact to be updated (or q to quit): ").strip())

            if search_query == 'q':
                print('Quiting.\n')
                break

            matches = []
            for contact in self.contacts:
                query_name = ''.join(search_query.lower().split())
                full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                if query_name in full_name:
                    matches.append(contact)

            if not matches:
                print("No contact matches the query. Please try again.\n")
                continue
            else:
                self.print_contact_list(matches)

            index = -2
            while index < -1 or index >= len(matches):
                try:
                    index = int(input("Enter the index of the contact to update (or -1 to quit): ").strip())
                    if index < -1 or index >= len(matches):
                        print("Invalid index. Please try again.\n")
                except ValueError:
                    print("Invalid index. Please try again.\n")
            if index == -1:
                print("Quiting.\n")
                continue
            contact_to_update = matches[index]

            print("\nThe contact to update is:")
            self.print_contact(contact_to_update)

            field_index = 'invalid'
            while not field_index == 'q':
                print("Which field do you want to update?")
                print("1. First Name")
                print("2. Last Name")
                print("3. Phone Number")
                print("4. Email Address")
                print("5. Address")
                field_index = input("Enter the index of the field to update (or q to quit): ").strip()

                while field_index not in ['q', '1', '2', '3', '4', '5']:
                    field_index = input("Invalid index. Please try again: ").strip()

                if field_index == 'q':
                    print("Quiting.\n")
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
                print()

                if field_index == '1':
                    old_value = contact_to_update.get_first_name()
                    if not old_value == new_value:
                        if self.is_contact_exist(new_value, contact_to_update.get_last_name()):
                            print(f"Failed to update contact. Contact '{new_value} {contact_to_update.get_last_name()}' already exists.\n")
                            continue
                    contact_to_update.set_first_name(new_value)
                elif field_index == '2':
                    old_value = contact_to_update.get_last_name()
                    if not old_value == new_value:
                        if self.is_contact_exist(contact_to_update.get_first_name(), new_value):
                            print(f"Failed to update contact. Contact '{contact_to_update.get_first_name()} {new_value}' already exists.\n")
                            continue
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
            print("3. Delete all contacts")
            print("Or enter q to quit.")
            choice = input("Enter your choice (1/2/3/q): ").strip()

            while choice not in ['1', '2', '3', 'q']:
                choice = input("Invalid choice. Please enter a valid option: ").strip()

            if choice == 'q':
                print("Quiting.\n")
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

                    index = -2
                    while index < -1 or index >= len(matches):
                        try:
                            index = int(input("Enter the index of the contact to delete (or -1 to quit): ").strip())
                            if index < -1 or index >= len(matches):
                                print("Invalid index. Please try again.\n")
                        except ValueError:
                            print("Invalid index. Please try again.\n")
                    if index == -1:
                        print("Quiting.\n")
                        continue
                    contact_to_delete = matches[index]
                    
                    delete_name = f"{contact_to_delete.get_first_name()} {contact_to_delete.get_last_name()}"
                    self.contacts.remove(contact_to_delete)
                    print(f"Contact '{delete_name}' deleted\n")

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
                                        if contact_full_name.lower() == full_name.lower():
                                            self.contacts.remove(contact)
                                            print(f"[Succeeded] Contact '{contact_full_name}' deleted")
                                            successful_deletions += 1
                                            found = True
                                            break
                                    if not found:
                                        print(f"[Failed] Contact '{full_name}' not found")
                        print(f"Batch delete completed: {successful_deletions}/{attempted_deletions} contacts deleted successfully.\n")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")

            elif choice == '3':
                self.delete_all_contacts()

    def delete_all_contacts(self):
        choice = input("Are you sure you want to delete all contacts? (yes/no): ").strip().lower()

        while choice not in ['yes', 'no']:
            choice = input("Invalid choice. Please enter yes or no: ").strip().lower()
        
        if choice == 'yes':
            self.contacts.clear()
            print("All contacts deleted.")
        print()

    def sort_contacts(self):
        while True:
            print("Do you want to sort contacts by:")
            print("1. First Name")
            print("2. Last Name")
            print("3. Phone Number")
            print("4. Create Time")
            print("5. Update Time")
            print("Or enter q to quit.")
            sort_choice = input("Enter your choice (1/2/3/4/5/q): ").strip()

            while sort_choice not in ['1', '2', '3', '4', '5', 'q']:
                sort_choice = input("Invalid choice. Please enter a valid option: ").strip()

            if sort_choice == 'q':
                print("Quiting.\n")
                return

            print("\nSelect a sort order:")
            if sort_choice in ['1', '2']:
                print("1. Alphabetically Up")
                print("2. Alphabetically Down")
            elif sort_choice in ['3']:
                print("1. Numerically Up")
                print("2. Numerically Down")
            else:
                print("1. Oldest first")
                print("2. Latest first")
            order_choice = input("Enter your choice (1/2): ").strip()

            while order_choice not in ['1', '2']:
                order_choice = input("Invalid choice. Please enter a valid option: ").strip()

            reverse = (order_choice == '2')
            show_create_time = (sort_choice == '4')
            show_update_time = (sort_choice == '5')

            if sort_choice == '1':
                self.contacts.sort(key=lambda contact: contact.get_first_name().lower(), reverse=reverse)
            elif sort_choice == '2':
                self.contacts.sort(key=lambda contact: contact.get_last_name().lower(), reverse=reverse)
            elif sort_choice == '3':
                self.contacts.sort(key=lambda contact: int(re.sub(r'\D', '', contact.get_phone_number())), reverse=reverse)
            elif sort_choice == '4':
                self.contacts.sort(key=lambda contact: contact.get_create_time(), reverse=reverse)
            elif sort_choice == '5':
                self.contacts.sort(key=lambda contact: contact.get_update_time(), reverse=reverse)

            print("\nContacts sorted successfully. Here are the first few contacts: ")
            self.print_contact_list(self.contacts[:5], False, show_create_time, show_update_time)

            show_more = input("Do you want to see the whole list? Enter 1 to show more or q to quit: ").strip()
            while show_more not in ['1', 'q']:
                show_more = input("Invalid choice. Please enter 1 or q: ").strip()
            
            if show_more == '1':
                self.print_contact_list(self.contacts[5:], False, show_create_time, show_update_time)
            
            print()

    def group_contacts(self):
        print("Group contacts by:")
        print("1. First letter of last name")
        print("Or enter 'q' to quit.")
        choice = input("Enter your choice (1/q): ").strip()

        while choice not in ['1', 'q']:
            choice = input("Invalid choice. Please enter a valid option: ").strip()

        if choice == 'q':
            print("Quiting.\n")
            return

        # Group contacts by the first letter of last name
        grouped_contacts = defaultdict(list)
        for contact in self.contacts:
            first_letter = contact.get_last_name()[0].upper()
            grouped_contacts[first_letter].append(contact)

        # Sort the dictionary by keys alphabetically (first letters)
        sorted_grouped_contacts = dict(sorted(grouped_contacts.items()))

        print("\nContacts grouped successfully. Displaying groups:")
        # Print each group of contacts
        for letter, contacts in sorted_grouped_contacts.items():
            print(f"{letter}")
            headers = ["First Name", "Last Name", "Phone Number", "Email Address", "Address"]
            rows = [[contact.get_first_name(), contact.get_last_name(), contact.get_phone_number(), 
                        contact.get_email_address(), contact.get_address()] for contact in contacts]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        print()

    def export_contacts_to_json(self, file_path):
        contacts_data = [contact.to_dict() for contact in self.contacts]
        with open(file_path, 'w') as json_file:
            json.dump(contacts_data, json_file, indent=4)
        print(f"Contacts successfully exported to {file_path}")

    def import_contacts_from_json(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                contacts_data = json.load(json_file)
                self.contacts = [Contact.from_dict(contact) for contact in contacts_data]
            print(f"Contacts successfully imported from {file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.")

phone_book = PhoneBook()
phone_book.import_contacts_from_json('database.json')
#phone_book.create_contact()
phone_book.print_all_contacts()
#phone_book.update_contact()
#phone_book.search_contact()
#phone_book.update_contact()
phone_book.delete_contact()
#phone_book.print_all_contacts()
phone_book.sort_contacts()
#phone_book.group_contacts()
#phone_book.search_contacts_by_date()
phone_book.export_contacts_to_json('database.json')

'''
Todo:
- Recording all operations performed in the application along with timestamps
- (Exporting to csv)

- Application script

To improve:
- Grouping
- Delete all
- Confirm update
'''