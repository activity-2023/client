import argparse
import socket
import tomllib

import structlog

import client.error as error

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
            self.client_socket.connect((Client.HOST_ADDRESS, Client.HOST_PORT))
            self.client_socket.settimeout(10)
        except ConnectionRefusedError:
            raise error.ConnectError(Client.HOST_ADDRESS, Client.HOST_PORT)

    def populate_params(self):
        Client.HOST_ADDRESS = self.config["network"]["host_address"]
        Client.HOST_PORT = self.config["network"]["host_port"]


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    cli_config_group = parser.add_argument_group()

    client_type_group = cli_config_group.add_mutually_exclusive_group()
    client_type_group.add_argument("-r", "--room",
                                   help="If the client is a room.",
                                   action="store_true")
    client_type_group.add_argument("-b", "--building",
                                   help="If the client is a building",
                                   action="store_true")
    cli_config_group.add_argument("--id",
                                  help="The ID of the client.",
                                  metavar="CLIENT_ID",
                                  type=int)
    cli_config_group.add_argument("--host",
                                  help="The IPv4 address of the server.",
                                  metavar="SERVER_IP",
                                  type=str)
    cli_config_group.add_argument("-p", "--port",
                                  help="The port of the server.",
                                  metavar="SERVER_PORT",
                                  type=int)

    parser.add_argument("--config",
                        default="./config.toml",
                        help="The path to the configuration file.",
                        metavar="PATH_TO_CONFIG",
                        type=str)

    return parser.parse_args()


def args_to_dict(args: argparse.Namespace) -> dict:
    return dict(
        client=dict(
            client_type='ROOM' if args.room else 'BUILDING',
            client_id=args.id
        ),
        network=dict(
            host_address=args.host,
            host_port=args.port
        )
    )


def main():
    client: Client
    args = get_cli_args()
    logger.debug("CLI arguments parsed.")

    try:
        with open(args.config, "rb") as f:
            config = tomllib.load(f)
            logger.debug("Configuration file found.")
            client = Client(config)
    except OSError as e:
        logger.error(f"An error occurred when trying to load the configuration from the file: {e}")
        logger.info("Loading configuration from the arguments...")
        client = Client(args_to_dict(args))
    finally:
        client()
