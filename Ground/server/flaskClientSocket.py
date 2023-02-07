import logging
import socket
from time import sleep

MSG_END = "MSG_END"


class FlaskClientSocket:

    def __init__(self, host, port, tries_max=9, tries_delay=5):
        self.socket = socket.socket()
        self.host = host
        self.port = port

        self.tries_max = tries_max
        self.tries_done = 0
        self.tries_delay = tries_delay

        self.connected = False
        self.end_connection = False

    def connect(self) -> bool:
        """Connect to socket server, retry if connection fails

        :return: True if socket connection established, else False
        """
        logging.info(f"Attempting to connect to {self.socket}:{self.host}")
        attempted_connections = 0
        while attempted_connections < self.tries_max:
            try:
                logging.info(f"\t#{attempted_connections} Connecting...")
                self.socket.connect((self.host, self.port))
                self.connected = True
                logging.info("\tConnection Successful")
                break
            except socket.error:
                logging.info(f"\tConnection Failed: {socket.error}")
                self.connected = False
                sleep(self.tries_delay)
                attempted_connections += 1
        return self.connected

    def end_connection(self) -> None:
        """Close socket connection

        :return: None
        """
        logging.info("Closing connection")
        self.socket.close()
        self.connected = False

    def send_message(self, message) -> bool:
        """Sends message to socket server, adding message ending signifier
        Retries sending or reattempts connection if message fails to send

        :param message: (str) message to send
        :return: True is message sending successful, else False
        """
        message_to_send = message + MSG_END
        successful_send = False
        msg_send_attempts = 0
        while not successful_send and msg_send_attempts < self.tries_max:
            try:
                logging.info(f"Sending message: {message_to_send}")
                self.socket.sendall(message_to_send.encode())
                successful_send = True
            except socket.error:
                logging.info(f"\tError Sending: {socket.error}")
                msg_send_attempts += 1
                # Check connection
                self.connect()
        return successful_send

