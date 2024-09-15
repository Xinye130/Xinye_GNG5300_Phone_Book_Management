import datetime

class Contact:
    def __init__(self, first_name = '', last_name = '', phone_number = '', email_address = '', address = ''):
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number
        self._email_address = email_address
        self._address = address
        self._create_time = datetime.datetime.now()
        self._update_time = self._create_time

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        if self._first_name != first_name:
            print("First name changed from", self._first_name, "to", first_name)
            self._first_name = first_name
            self._update_time = datetime.datetime.now()
        else:
            print("No changes were made to the first name.")

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        if self._last_name != last_name:
            print("Last name changed from", self._last_name, "to", last_name)
            self._last_name = last_name
            self._update_time = datetime.datetime.now()
        else:
            print("No changes were made to the last name.")

    def get_phone_number(self):
        return self._phone_number

    def set_phone_number(self, phone_number):
        if self._phone_number != phone_number:
            print("Phone number changed from", self._phone_number, "to", phone_number)
            self._phone_number = phone_number
            self._update_time = datetime.datetime.now()
        else:
            print("No changes were made to the phone number.")

    def get_email_address(self):
        return self._email_address

    def set_email_address(self, email_address):
        if self._email_address != email_address:
            print("Email address changed from", self._email_address, "to", email_address)
            self._email_address = email_address
            self._update_time = datetime.datetime.now()
        else:
            print("No changes were made to the email address.")

    def get_address(self):
        return self._address

    def set_address(self, address):
        if self._address != address:
            print("Address changed from", self._address, "to", address)
            self._address = address
            self._update_time = datetime.datetime.now()
        else:
            print("No changes were made to the address.")

    def get_create_time(self):
        return self._create_time

    def get_update_time(self):
        return self._update_time