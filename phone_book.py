from contact import Contact
from tabulate import tabulate
import csv
import json
import re
from collections import defaultdict
from datetime import datetime
import logging

class PhoneBook:
    '''
    Class to represent a phone book that stores contacts
    '''
    logger = logging.getLogger("phoneBookLogger")

    def __init__(self):
        ''' 
        Initialize the PhoneBook object with an empty list to store contacts
        '''
        self.contacts = []

    def print_all_contacts(self):
        '''
        Print all contacts in the phone book in a tabular format
        '''
        print("[Print All Contacts]")
        self.logger.info("Print all contacts")
        
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
        '''
        Print a list of contacts in a tabular format
        Optionally show the index of each contact, the create time, or the update time
        '''
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
        '''
        Check if the email address is valid using regular expressions
        '''
        if email == "":
            return True
        
        # Regular expression for validating an email address: (user_name)@(domain_name).(top-leveldomain)  
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email) is not None
    
    def is_valid_phone_number(self, phone_number):
        '''
        Check if the phone number is valid using regular expressions
        Phone number should be in the format (###) ###-####
        '''
        # Regular expression for validating a phone number: (###) ###-####
        phone_number_regex = re.compile(r'\(\d{3}\) \d{3}-\d{4}')
        return re.fullmatch(phone_number_regex, phone_number) is not None
    
    def is_contact_exist(self, first_name, last_name):
        '''
        Check if a contact with the given first name and last name already exists in the phone book
        '''
        full_name_to_check = f"{first_name.lower()} {last_name.lower()}"
        for contact in self.contacts:
            full_name = f"{contact.get_first_name().lower()} {contact.get_last_name().lower()}"
            if full_name == full_name_to_check:
                return True
        return False

    def input_mandatory_field(self, value):
        '''
        Prompt the user to enter a mandatory field until a valid value is provided
        '''
        while value == "":
            value = input("Mandatory field. Please enter a valid value: ").strip()
        return value
 
    def create_contact(self):
        '''
        Create a new contact by entering the contact details manually or importing from a CSV file
        Perform validation checks for phone number, email address, and duplicated contacts
        '''
        print("[Create Contact]")
        self.logger.info("Start create contact")
        while True:
            print("How would you like to add contacts:")
            print("1. Add contact manually")
            print("2. Import contacts from CSV")
            print("Or enter q to quit.")
            choice = input("Enter your choice (1/2/q): ")

            if choice == '1':
                # Input and validate contact details
                first_name = self.input_mandatory_field(input("Enter first name: ").strip())
                last_name = self.input_mandatory_field(input("Enter last name: ").strip())
                phone_number = self.input_mandatory_field(input("Enter phone number in the format (###) ###-####: ").strip())
                while not self.is_valid_phone_number(phone_number):
                    phone_number = input("Invalid phone number. Please try again: ").strip()
                email_address = input("Enter email address (or press Enter to skip): ").strip()
                while not self.is_valid_email(email_address):
                    email_address = input("Invalid email address. Please try again: ").strip()
                address = input("Enter address (or press Enter to skip): ").strip()

                # Check for duplicated contacts
                if not self.is_contact_exist(first_name, last_name):
                    new_contact = Contact(first_name, last_name, phone_number, email_address, address)
                    self.contacts.append(new_contact)
                    print(f"Contact added: {first_name} {last_name}, {phone_number}, {email_address}, {address}\n")
                else:
                    print(f"Failed to add contact. Contact '{first_name} {last_name}' already exists.\n")
                    continue

            elif choice == '2':
                csv_file = input("Enter the path to the CSV file: ")
                self.logger.info(f"Start batch add contacts from {csv_file}")
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
                                self.logger.info("Contact addition failed: " + error_message)
                        print(f"Batch addition completed: {successful_additions}/{attempted_additions} contacts added successfully.\n")
                        self.logger.info(f"Batch addition completed: {successful_additions}/{attempted_additions} contacts added successfully")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")
                    self.logger.info("Batch addition failed: CSV file not found")

            elif choice == 'q':
                print("Quiting.\n")
                self.logger.info("Quit Create Contact")
                break

            else:
                print("Invalid choice. Please try again.\n")

    def search_contact(self):
        '''
        Search for contacts by full name, phone number, or date created
        Display the search results and allow the user to view the history of changes for a specific contact
        Support partial match for full name and phone number
        '''
        print("[Search Contact]")
        self.logger.info("Start search for contacts")
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
                self.logger.info("Quit search for contacts")
                break

            matches = []
            show_create_time = False
            if search_type in ['1', '2']:
                search_query = self.input_mandatory_field(input("Enter the search query (partial match supported): ").strip()) 
                
                if search_type == '1':
                    self.logger.info(f"Search by full name: {search_query}")
                elif search_type == '2':
                    self.logger.info(f"Search by phone number: {search_query}")

                for contact in self.contacts:
                    if search_type == '1':
                        query_name = ''.join(search_query.lower().split())
                        full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                        if query_name in full_name:
                            matches.append(contact)
                    elif search_type == '2':
                        query_number = re.sub(r'\D', '', search_query)
                        phone_number = re.sub(r'\D', '', contact.get_phone_number())
                        if not query_number == "" and query_number in phone_number:
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
            self.logger.info("View history of changes")

    def search_contacts_by_date(self):
        '''
        Search for contacts by the date created
        Allow the user to enter a single date or a date range
        Return a list of contacts that were created within the specified date range
        '''
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
                    # Validate the date format
                    start_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
                    end_date = datetime.strptime(dates[1], '%Y-%m-%d').date()
                    is_valid_date = True
                except ValueError:
                    dates = input("Invalid date format. Please try again: ").strip().split()
            
            else:
                dates = input("Invalid date format. Please try again: ").strip().split()

        self.logger.info(f"Search by creation date: {start_date} to {end_date}")
        for contact in self.contacts:
            create_time = contact.get_create_time().date()
            if start_date <= create_time <= end_date:
                matches.append(contact)
        
        return matches

    def update_contact(self):
        '''
        Update an existing contact by selecting the contact to update and the field to modify
        Allow the user to update the first name, last name, phone number, email address, or address
        Perform validation checks for phone number, email address, and duplicated contacts
        '''
        print("[Update Contact]")
        self.logger.info("Start update contact")
        while True:
            print("Update contact")
            search_query = self.input_mandatory_field(input("Enter the name of the contact to be updated (or q to quit): ").strip())

            if search_query == 'q':
                print('Quiting.\n')
                self.logger.info("Quit update contact")
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
            self.logger.info(f"Start update contact: {contact_to_update.get_first_name()} {contact_to_update.get_last_name()}, {contact_to_update.get_phone_number()}, {contact_to_update.get_email_address()}, {contact_to_update.get_address()}")

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
                    self.logger.info(f"Finish update contact. Contact is now: {contact_to_update.get_first_name()} {contact_to_update.get_last_name()}, {contact_to_update.get_phone_number()}, {contact_to_update.get_email_address()}, {contact_to_update.get_address()}")
                    break
                
                # Verity mandatory fields, validate phone number and email
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
                    # Check for duplicated contacts
                    old_value = contact_to_update.get_first_name()
                    if not old_value.lower() == new_value.lower():
                        if self.is_contact_exist(new_value, contact_to_update.get_last_name()):
                            print(f"Failed to update contact. Contact '{new_value} {contact_to_update.get_last_name()}' already exists.\n")
                            self.logger.info(f"Failed to update contact: Contact '{new_value} {contact_to_update.get_last_name()}' already exists")
                            continue
                    contact_to_update.set_first_name(new_value)
                elif field_index == '2':
                    # Check for duplicated contacts
                    old_value = contact_to_update.get_last_name()
                    if not old_value.lower() == new_value.lower():
                        if self.is_contact_exist(contact_to_update.get_first_name(), new_value):
                            print(f"Failed to update contact. Contact '{contact_to_update.get_first_name()} {new_value}' already exists.\n")
                            self.logger.info(f"Failed to update contact: Contact '{contact_to_update.get_first_name()} {new_value}' already exists")
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
        '''
        Provide options to delete a single contact, multiple contacts, or all contacts
        For manually delete, search for the contact by name and select the contact to delete
        '''
        print("[Delete Contact]")
        self.logger.info("Start delete contact")
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
                self.logger.info("Quit delete contact")
                break

            elif choice == '1':
                delete_query = self.input_mandatory_field(input("Enter the name of the contact to delete: ").strip())
                self.logger.info(f"Try to delete contact: {delete_query}")

                # Search for the contact to delete by name
                matches = []
                for contact in self.contacts:
                    query_name = ''.join(delete_query.lower().split())
                    full_name = ''.join(f"{contact.get_first_name()} {contact.get_last_name()}".lower().split())
                    if query_name in full_name:
                        matches.append(contact)

                if not matches:
                    print(f"Contact '{delete_query}' not found.\n")
                    self.logger.info(f"Contact '{delete_query}' not found")
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
                        self.logger.info(f"Quit delete contact: {delete_query}")
                        continue
                    contact_to_delete = matches[index]
                    
                    delete_name = f"{contact_to_delete.get_first_name()} {contact_to_delete.get_last_name()}"
                    self.contacts.remove(contact_to_delete)
                    print(f"Contact '{delete_name}' deleted\n")
                    self.logger.info(f"Contact deleted: {delete_name}")

            elif choice == '2':
                csv_file = input("Enter the path to the CSV file: ").strip()
                self.logger.info(f"Start batch delete contacts from {csv_file}")
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
                                        # Name should be exactly matches, case-insensitive
                                        contact_full_name = f"{contact.get_first_name()} {contact.get_last_name()}"
                                        if contact_full_name.lower() == full_name.lower():
                                            self.contacts.remove(contact)
                                            print(f"[Succeeded] Contact '{contact_full_name}' deleted")
                                            self.logger.info(f"Contact deleted: {contact_full_name}")
                                            successful_deletions += 1
                                            found = True
                                            break
                                    if not found:
                                        print(f"[Failed] Contact '{full_name}' not found")
                                        self.logger.info(f"Contact not found: {full_name}")
                        print(f"Batch delete completed: {successful_deletions}/{attempted_deletions} contacts deleted successfully.\n")
                        self.logger.info(f"Batch delete completed: {successful_deletions}/{attempted_deletions} contacts deleted successfully")
                except FileNotFoundError:
                    print("CSV file not found. Please try again.\n")
                    self.logger.info("Batch delete failed: CSV file not found")

            elif choice == '3':
                self.delete_all_contacts()

    def delete_all_contacts(self):
        '''
        Delete all contacts in the phone book after confirming with the user
        '''
        choice = input("Are you sure you want to delete all contacts? (yes/no): ").strip().lower()
        self.logger.info("Try to delete all contacts")

        while choice not in ['yes', 'no']:
            choice = input("Invalid choice. Please enter yes or no: ").strip().lower()
        
        if choice == 'yes':
            self.contacts.clear()
            print("All contacts deleted.")
            self.logger.info("All contacts deleted\n")
        else:
            print()
            self.logger.info("Quit delete all contacts")

    def sort_contacts(self):
        '''
        Sort the contacts by first name, last name, phone number, create time, or update time
        Allow the user to choose the sort order (ascending or descending)
        '''
        print("[Sort Contact]")
        self.logger.info("Start sort contacts")
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
                self.logger.info("Quit sort contacts")
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
            order = "descending" if reverse else "ascending"
            show_create_time = (sort_choice == '4')
            show_update_time = (sort_choice == '5')

            if sort_choice == '1':
                self.contacts.sort(key=lambda contact: contact.get_first_name().lower(), reverse=reverse)
                self.logger.info(f"Sorted contacts by first name {order}")
            elif sort_choice == '2':
                self.contacts.sort(key=lambda contact: contact.get_last_name().lower(), reverse=reverse)
                self.logger.info(f"Sorted contacts by last name {order}")
            elif sort_choice == '3':
                self.contacts.sort(key=lambda contact: int(re.sub(r'\D', '', contact.get_phone_number())), reverse=reverse)
                self.logger.info(f"Sorted contacts by phone number {order}")
            elif sort_choice == '4':
                self.contacts.sort(key=lambda contact: contact.get_create_time(), reverse=reverse)
                self.logger.info(f"Sorted contacts by create time {order}")
            elif sort_choice == '5':
                self.contacts.sort(key=lambda contact: contact.get_update_time(), reverse=reverse)
                self.logger.info(f"Sorted contacts by update time {order}")

            # Display the first few contacts after sorting
            print("\nContacts sorted successfully. Here are the first few contacts: ")
            self.print_contact_list(self.contacts[:5], False, show_create_time, show_update_time)

            # Ask the user if they want to see the whole list
            show_more = input("Do you want to see the whole list? Enter 1 to show more or q to quit: ").strip()
            while show_more not in ['1', 'q']:
                show_more = input("Invalid choice. Please enter 1 or q: ").strip()
            
            if show_more == '1':
                self.print_contact_list(self.contacts[5:], False, show_create_time, show_update_time)
            
            print()

    def group_contacts(self):
        '''
        Group the contacts by the first letter of the last name
        Display the groups of contacts in a tabular format
        '''
        print("[Group Contact]")
        self.logger.info("Start group contacts")
        print("Group contacts by:")
        print("1. First letter of last name")
        print("Or enter 'q' to quit.")
        choice = input("Enter your choice (1/q): ").strip()

        while choice not in ['1', 'q']:
            choice = input("Invalid choice. Please enter a valid option: ").strip()

        if choice == 'q':
            print("Quiting.\n")
            self.logger.info("Quit group contacts")
            return

        # Group contacts by the first letter of last name
        grouped_contacts = defaultdict(list)
        for contact in self.contacts:
            first_letter = contact.get_last_name()[0].upper()
            grouped_contacts[first_letter].append(contact)
        self.logger.info("Grouped contacts by first letter of last name")

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
        self.logger.info("Quit group contacts")

    def export_contacts_to_json(self, file_path):
        '''
        Export the contacts to a JSON file
        '''
        self.logger.info(f"Export contacts to {file_path}")
        contacts_data = [contact.to_dict() for contact in self.contacts]
        with open(file_path, 'w') as json_file:
            json.dump(contacts_data, json_file, indent=4)
        print(f"Contacts successfully exported to {file_path}")
        self.logger.info(f"Contacts exported to {file_path}")

    def import_contacts_from_json(self, file_path):
        '''
        Import contacts from a JSON file
        '''
        self.logger.info(f"Import contacts from {file_path}")
        try:
            with open(file_path, 'r') as json_file:
                contacts_data = json.load(json_file)
                self.contacts = [Contact.from_dict(contact) for contact in contacts_data]
            print(f"Contacts successfully imported from {file_path}")
            self.logger.info(f"Contacts imported from {file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            self.logger.info(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.")
            self.logger.info(f"Error decoding JSON from file {file_path}.")