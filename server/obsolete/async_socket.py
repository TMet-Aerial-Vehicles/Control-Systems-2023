import asyncore
import logging
import socket
from time import sleep


class FlaskClientSocketASYNC(asyncore.dispatcher_with_send):

    def __init__(self, host, port, tries_max=10, tries_delay=10):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port

        self.tries_max = tries_max
        self.tries_done = 0
        self.tries_delay = tries_delay

        self.end_connection = False
        self.out_buffer = ""  # Buffer for sending.

        self.reconnect()  # Initial connection.

    def reconnect(self):
        if self.tries_done == self.tries_max:
            self.end_connection = True
            return

        print('Trying connecting in {} sec...'.format(self.tries_delay))
        sleep(self.tries_delay)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect((self.host, self.port))
        except socket.error:
            pass

        if not self.connected:
            self.tries_done += 1
            print('Could not connect for {} time(s).'.format(self.tries_done))

    def handle_connect(self):
        self.tries_done = 0
        print('We connected and can get the stuff done!')

    def handle_read(self):
        # Flask will only write to socket
        return

    def handle_close(self):
        print('Connection closed.')
        self.close()

        if not self.end_connection:
            self.reconnect()

    def end_connection(self):
        self.end_connection = True
        self.close()

    def do_connect(self):
        try:
            logging.info(f"Attempting to connect to {self.socket}:{self.host}")
            self.socket.connect((self.host, self.port))
            self.connected = True
        except socket.error:
            self.connected = False
            attempted_connections = 0
            while not self.connected and attempted_connections < self.tries_max:
                logging.info("\tAttempting to connect...")
                try:
                    self.socket.connect((self.host, self.port))
                    self.connected = True
                except socket.error:
                    sleep(self.tries_delay)
                    attempted_connections += 1
