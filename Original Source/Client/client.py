# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

"""All the functions that a user can perform.
   The client object gets instantiated and used in ui.py"""

import socket
import json
import time
import os,sys

class Client:

    def __init__(self):
        """
        Creates a socket for the client, connects to server
        """

        host = 'localhost'
        port = 8787
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))

    def login(self, username, pword):
        """
        Logs the user in once connected to the server

        :param username: user's name
        :param pword: user's password

        :return: 0 if username doesn't exist or incorrect password OR
                 1 if username exists and enters correct password
        """

        # serialize the username and pword into json
        info = json.dumps({'type': 'login',
                           'username': username,
                           'pword': pword})

        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def register(self, username, pword):
        '''
        Registers a new user

        :param username: new user name
        :param pword: new user password (encrypyted)

        :return: 0 if username is not unique (can't have duplicate usernames)
                 1 if username is unique and user is put in db
        '''

        # serialize the username and pword into json
        info = json.dumps({'type': 'register',
                           'username': username,
                           'pword': pword})

        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def upload(self, fileName, category, keywords):
		# KH -- EXCISED PER LICENSING RESTRICTION

    def delete(self, fileName):
        """
        Asks the data_retriever to delete a file

        :param fileName: name of the file you want deleted
        """

        info = json.dumps({'type':'delete',
                           'fileName': fileName})

        self.sock.send(info.encode())


    def search(self, query):
		# KH -- EXCISED PER LICENSING RESTRICTION

    def download(self, fileName):
        """
        Asks the data_retriever to search an existing file in the db

        :param fileName: name of file

        :return: contents of file, or an error msg if file doesn't exist
        """
        info = json.dumps({'type':'download','fileName':fileName})

        self.sock.send(info.encode())

        flag = self.sock.recv(1024).decode()
        if flag == 'SOF':
            self.retrieveFile(fileName)
            return 1

    def retrieveQuery(self,query):
            data = self.sock.recv(1024).decode()
            #keep recieving until EOQ
            while(True):
                if sys.getsizeof(data)<1:
                    return 0
                else:
                    data = self.sock.recv(1024).decode()
                    print(data+"\n")
                    return 1

    def retrieveFile(self,fileName):
            # create the file on client side
            file = open('downloads/' + fileName, 'w')
            data = self.sock.recv(1024).decode()

            #keep recieving until EOF
            while(True):
                data = self.sock.recv(1024).decode()

                if data == 'EOF':
                    file.close()
                    break
                else:
                    file.write(data)
            file.close()
