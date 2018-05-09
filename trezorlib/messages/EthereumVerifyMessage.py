# Automatically generated by pb2py
from .. import protobuf as p


class EthereumVerifyMessage(p.MessageType):
    MESSAGE_WIRE_TYPE = 65
    FIELDS = {
        1: ('address', p.BytesType, 0),
        2: ('signature', p.BytesType, 0),
        3: ('message', p.BytesType, 0),
    }

    def __init__(
        self,
        address: bytes = None,
        signature: bytes = None,
        message: bytes = None
    ) -> None:
        self.address = address
        self.signature = signature
        self.message = message
