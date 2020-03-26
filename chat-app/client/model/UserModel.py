# This Python file uses the following encoding: utf-8
from PySide2 import QtQuick
from PySide2.QtCore import QAbstractListModel, Qt, Slot, QModelIndex, QObject
import requests
from datetime import datetime

class User(QObject):
    def __init__(self):
        super().__init__()
        self.id = None
        self.last_accessed_dt = None
        self.logged_in = False


    @Slot(str, str, result=str)
    def login(self, user_name, password):
        ''' Call user/login API with user_name and password, returns True if correct '''
        ''' Returns tuples (True, 'OK') or (False, message) '''
        payload = {
                    'user_name' : user_name,
                    'password' : password,
        }

        url = "http://127.0.0.1:8089/user/login"
        response = requests.post(url, json=payload)
        status, message = self.log_in_user(response)
        print('{},{}'.format(status, message))
        return '{},{}'.format(status, message)

    @Slot(str, str, str, str, str, str, str, result=str)
    def register(self, user_name, first_name, last_name, nick, email, password, confirm_password):
        ''' Call user/create API register new user, log him in, returns True if correct, False with issues '''
        ''' Returns tuples (True, 'OK') or (False, message) '''
        payload = {
                    'user_name' : user_name,
                    'password' : password,
                    'first_name': first_name,
                    'last_name' : last_name,
                    'email'     : email,
                    'nick'      : nick

        }

        url = "http://127.0.0.1:8089/user/create"
        response = requests.post(url, json=payload)
        status, message = self.log_in_user(response)
        return  'OK'
        #return '{},{}'.format(status, message)

    def log_in_user(self, response):
        ''' Auxiliary class for both login and register
            Returns true if user should be logged in, False otherwise
        '''
        json = response.json()
        if str(response.status_code) == '200':
            self.id = json['200']
            self.last_accessed_dt = datetime.now()
            self.logged_in = True
            print('logged_in')
            return True, 'OK'

        return False, json['Message']
