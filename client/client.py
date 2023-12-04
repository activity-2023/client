import getpass
import re
import socket

import structlog

from client.error import IncorrectId, BadPassword
import client.network

logger = structlog.get_logger()


class Client:
    HOST_ADDRESS = "127.0.0.1"
    HOST_PORT = 54321

    def __init__(self, config: dict, sock: socket.socket = None):
        self.config = config
        if sock is None:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logger.info("Default IPv4 socket created.")
        else:
            self.client_socket = sock

        self.populate_params()

    def __call__(self, *args, **kwargs):
        self.start()

    def start(self):
        try:
            person_id = int(input("Please enter your ID: "))
            if person_id < 1 or person_id > 2147483647:
                raise IncorrectId(f"The person_id {person_id} is not correct. Please try again.")

            pin = getpass.getpass("Please enter your PIN: ")
            pattern = re.compile(r"^[0-9]{4}$")
            if not pattern.fullmatch(pin):
                raise BadPassword("Incorrect password! Try again.")

            self.client_socket.settimeout(5)
            self.client_socket.connect((Client.HOST_ADDRESS, Client.HOST_PORT))

            client.network.process(self.client_socket, self.config, person_id, pin)
        except ConnectionRefusedError:
            logger.critical(f"Connection refused by {Client.HOST_ADDRESS}:{Client.HOST_PORT}. The server may be down.")
        except ValueError:
            print("Wrong ID., please try again.")
        except BadPassword:
            print("Wrong password, please try again.")
        except IncorrectId:
            print("You are not allowed to enter here.")
        except TimeoutError:
            logger.error("The client is taking too long to respond.")

    def populate_params(self):
        Client.HOST_ADDRESS = self.config["host_address"] if self.config["host_address"] else Client.HOST_ADDRESS
        Client.HOST_PORT = self.config["host_port"] if self.config["host_port"] else Client.HOST_PORT
