from enum import IntEnum, verify, UNIQUE
import hashlib
import socket

import structlog

from client.error import BadConfig, BadData, BadProtocol, IncorrectId, AccessError, BadPassword

logger = structlog.get_logger()


@verify(UNIQUE)
class ProtocolCode(IntEnum):
    DATAOK = 0x10
    FORMATOK = 0x11
    ACCESSOK = 0x12
    BADDATA = 0x20
    BADFORMAT = 0x21
    BADACCESS = 0x22
    ROOMID = 0x30
    BUILDINGID = 0x31
    PERSONID = 0x32
    NONCE = 0x33
    PASSWD = 0x34

    def __eq__(self, other):
        if isinstance(other, ProtocolCode):
            return self.value == other.value
        elif isinstance(other, bytes):
            return self.value.to_bytes(1, "big") == other
        else:
            return False


def net_code(code: ProtocolCode) -> bytes:
    return code.value.to_bytes(1, "big")


def process(sock: socket.socket, config: dict, person_id: int, pin: str) -> None:
    client_type: str = config["client_type"]
    client_id: int = config["client_id"]

    try:
        if client_type not in ["ROOM", "BUILDING"]:
            raise BadConfig(f"The client_type {client_type} is not supported.")

        if client_id < 1 or client_id > 2147483647:
            raise BadConfig(f"The client_id {client_id} is out of range.")

        to_send = bytearray()
        if client_type == "ROOM":
            to_send.extend(net_code(ProtocolCode.ROOMID))
        else:
            to_send.extend(net_code(ProtocolCode.BUILDINGID))

        to_send.extend(client_id.to_bytes(4, "big"))
        sock.sendall(to_send)

        data = sock.recv(1)
        if not (data == ProtocolCode.DATAOK):
            if data == ProtocolCode.BADDATA:
                raise BadData("Unknown client_id. Please change the configuration.")
            else:
                raise BadProtocol("Bad protocol!")

        to_send.clear()
        to_send.extend(net_code(ProtocolCode.PERSONID))
        to_send.extend(person_id.to_bytes(4, "big"))
        sock.sendall(to_send)

        data = sock.recv(1)
        if data == ProtocolCode.BADDATA:
            raise IncorrectId(f"The person with the ID {person_id} does not exist. Please try again.")

        if not (data == ProtocolCode.ACCESSOK):
            if data == ProtocolCode.BADACCESS:
                raise AccessError(f"The person with the ID {person_id} cannot access this room now.")
            else:
                raise BadProtocol("Bad protocol!")

        data = sock.recv(1)
        if not (data == ProtocolCode.NONCE):
            raise BadProtocol("Bad protocol!")

        data = sock.recv(6)
        nonce = data.decode()
        if not nonce.isdigit():
            raise BadProtocol("Bad protocol!")

        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        secured_hash = hashlib.sha256((pin_hash + nonce).encode()).digest()

        to_send.clear()
        to_send.extend(net_code(ProtocolCode.PASSWD))
        to_send.extend(secured_hash)
        sock.sendall(to_send)

        data = sock.recv(1)
        if data == ProtocolCode.DATAOK:
            print("Door is opened!")
        else:
            raise BadPassword("Incorrect password! Please try again.")
    except BadData as e:
        print("Incorrect data.")
        logger.error(e)
    except BadProtocol:
        logger.fatal("Protocol error!")
    except BadConfig:
        logger.fatal("Wrong configuration, please fix it and try again.")
    except BadPassword:
        print("Wrong password, please try again.")
    except IncorrectId:
        print("You are not allowed to enter here.")
    finally:
        sock.close()
