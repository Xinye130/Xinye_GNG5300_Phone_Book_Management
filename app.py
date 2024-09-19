from phone_book import PhoneBook
import logging

def init_logging():
    logging.basicConfig(
        filename='phonebook_log.log', 
        encoding='utf-8',
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG
    )

def main():
    '''
    Main function to run the Phone Book Management System
        - Initialize logging
        - Create a PhoneBook object
        - Import contacts from database.json
        - Display menu options
        - Perform actions based on user input
        - Export contacts to database.json before exiting
    '''
    init_logging()
    logger = logging.getLogger("phoneBookLogger")
    logger.info("Start Phone Book Management System")

    phone_book = PhoneBook()

    print("Entering phone book management system ...")
    print("Importing contacts ...")
    phone_book.import_contacts_from_json("database.json")
    print()

    while True:
        print("Welcome to Phone Book Management System!")
        print("1. Print all contacts")
        print("2. Create contact")
        print("3. Search contact and view history of change")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Sort contacts")
        print("7. Group contacts")
        print("Enter 'q' to quit.")
        
        choice = input("Enter your choice (1/2/3/4/5/6/7/q): ").strip()

        while choice not in ['1', '2', '3', '4', '5', '6', '7', 'q']:
            choice = input("Invalid choice. Please try again: ").strip()

        print()
        if choice == 'q':
            print("Exiting the Phone Book Management System ...")
            print("Exporting contacts ...")
            phone_book.export_contacts_to_json("database.json")
            logger.info("Exit Phone Book Management System")
            break
        elif choice == '1':
            phone_book.print_all_contacts()
        elif choice == '2':
            phone_book.create_contact()
        elif choice == '3':
            phone_book.search_contact()
        elif choice == '4':
            phone_book.update_contact()
        elif choice == '5':
            phone_book.delete_contact()
        elif choice == '6':
            phone_book.sort_contacts()
        elif choice == '7':
            phone_book.group_contacts()

if __name__ == "__main__":
    main()