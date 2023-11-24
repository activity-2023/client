import argparse

import structlog

from .client import Client
from .gui.gui import Gui

logger = structlog.get_logger()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    config = subparsers.add_parser("configure")
    config.set_defaults(command="configure")

    gui = subparsers.add_parser("gui")
    gui.set_defaults(command="gui")

    client_type_group = config.add_mutually_exclusive_group()
    client_type_group.add_argument("-r", "--room",
                                   help="If the client is a room.",
                                   action="store_true")
    client_type_group.add_argument("-b", "--building",
                                   help="If the client is a building",
                                   action="store_true")
    config.add_argument("--id",
                        help="The ID of the client.",
                        metavar="CLIENT_ID",
                        type=int)
    config.add_argument("--host",
                        help="The IPv4 address of the server.",
                        metavar="SERVER_IP",
                        type=str)
    config.add_argument("-p", "--port",
                        help="The port of the server.",
                        metavar="SERVER_PORT",
                        type=int)

    return parser.parse_args()


def main():
    args = get_args()
    logger.debug("Arguments parsed.")

    if args.command == "gui":
        gui = Gui()
        gui()
    elif args.command == "configure":
        client = Client(dict(
            host_address=args.host,
            host_port=args.port,
            client_type="ROOM" if args.room else "BUILDING",
            client_id=args.id
        ))
        client()
