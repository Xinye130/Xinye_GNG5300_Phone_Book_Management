import datetime

class Contact:
    def __init__(self, first_name='', last_name='', phone_number='', email_address='', address=''):
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number
        self._email_address = email_address
        self._address = address
        self._create_time = datetime.datetime.now()
        self._update_time = self._create_time
        self._history = []
        message = f'{first_name} {last_name}, {phone_number}, {email_address}, {address}'
        self._history.append(Change('Created', message, '', '', '', self._create_time))

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        if self._first_name != first_name:
            self._update_time = datetime.datetime.now()
            self._history.append(Change('Updated', '', 'First Name', self._first_name, first_name, self._update_time))
            print(f"First Name changed from '{self._first_name}' to '{first_name}'")
            self._first_name = first_name
        else:
            print("No changes made to First Name.")

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        if self._last_name != last_name:
            self._update_time = datetime.datetime.now()
            self._history.append(Change('Updated', '', 'Last Name', self._last_name, last_name, self._update_time))
            print(f"Last Name changed from '{self._last_name}' to '{last_name}'")
            self._last_name = last_name
        else:
            print("No changes made to Last Name.")

    def get_phone_number(self):
        return self._phone_number

    def set_phone_number(self, phone_number):
        if self._phone_number != phone_number:
            self._update_time = datetime.datetime.now()
            self._history.append(Change('Updated', '', 'Phone Number', self._phone_number, phone_number, self._update_time))
            print(f"Phone Number changed from '{self._phone_number}' to '{phone_number}'")
            self._phone_number = phone_number
        else:
            print("No changes made to Phone Number.")

    def get_email_address(self):
        return self._email_address

    def set_email_address(self, email_address):
        if self._email_address != email_address:
            self._update_time = datetime.datetime.now()
            self._history.append(Change('Updated', '', 'Email Address', self._email_address, email_address, self._update_time))
            print(f"Email Address changed from '{self._email_address}' to '{email_address}'")
            self._email_address = email_address
        else:
            print("No changes made to Email Address.")

    def get_address(self):
        return self._address

    def set_address(self, address):
        if self._address != address:
            self._update_time = datetime.datetime.now()
            self._history.append(Change('Updated', '', 'Address', self._address, address, self._update_time))
            print(f"Address changed from '{self._address}' to '{address}'")
            self._address = address        
        else:
            print("No changes made to Address.")

    def get_create_time(self):
        return self._create_time

    def get_update_time(self):
        return self._update_time
    
    def get_history(self): 
        return self._history
    
    def print_history(self):
        for change in self._history:
            change.print()

class Change:
    def __init__(self, operation='', message='', field='', old_value='', new_value='', change_time=''):
        self._operation = operation
        self._message = message
        self._field = field
        self._old_value = old_value
        self._new_value = new_value
        self._change_time = change_time
    
    def print(self):
        if self._operation == 'Created':
            print(f'{self._change_time} [{self._operation}] {self._message}')
        elif self._operation == 'Updated':
            print(f"{self._change_time} [{self._operation}] {self._field} from '{self._old_value}' to '{self._new_value}'")