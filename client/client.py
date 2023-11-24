import socket

import structlog

import client.error
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
            self.client_socket.settimeout(5)
            self.client_socket.connect((Client.HOST_ADDRESS, Client.HOST_PORT))

            client.network.process(self.client_socket, self.config)
        except ConnectionRefusedError as e:
            logger.critical(f"Connection refused by {Client.HOST_ADDRESS}:{Client.HOST_PORT}. The server may be down.")

    def populate_params(self):
        Client.HOST_ADDRESS = self.config["host_address"]
        Client.HOST_PORT = self.config["host_port"]
