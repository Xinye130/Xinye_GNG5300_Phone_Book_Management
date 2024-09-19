Before running
- Please install tabulate by: pip install tabulate

Executing program
- Under this directory, run: python app.py

Important files (please don't modify)
- database.json: stores added contacts information and history of changes. For testing purpose, it should have contained contact informations to be automatically imported after application starts. You may view these contacts using "1. Print all contacts". Some of them have attributes modified to demonstrate update functionality.
- phonebook_log.log: logs all application activities. For demonstration purpose, it should have contained several logs.

Testing
- Use add_new.csv to test batch create contacts
- Use add_invalid.csv to test batch create contacts validaion
- Use delete.csv to test batch delete and its validation
- Database contains contacts created and updated on 2024-09-19. You may use this date for searching contact by date

Rules
- This application uses full name (First Name + Last Name) to uniquely identify contacts. Duplicated contacts with the same name (case insensitive) are not allowed when creating and updating.
- For each contact, First Name, Last Name, and Phone Number are mandatory fields. Email Address and Address are optional, could be empty.
- Phone Number must be entered in the format (###) ###-####. This application does not accept any other format.
- Email Address should be in the format (user_name)@(domain_name).(top-leveldomain).
- Date should be in the format yyyy-mm-dd.
- Batch create (please reference add_old.csv): For csv file, each row should be: first_name, last_name, phone_number, email_address, address. The file should not contain header.
- Batch delete (please reference delete.csv): For csv file, each row should be: first_name, last_name. The file should not contain header. Batch delete does not support partial match, contact names should exactly match.
- Partial match supported in: Search Contact by name or phone number, search for contact to update in Update Contact, search for contact to be manually deleted in Delete Contact
- For every functionality, the application will prompt until the user enters a valid input or chooses to quit.
