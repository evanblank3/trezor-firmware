# Automatically generated by pb2py
from .. import protobuf as p


class NEMProvisionNamespace(p.MessageType):
    FIELDS = {
        1: ('namespace', p.UnicodeType, 0),
        2: ('parent', p.UnicodeType, 0),
        3: ('sink', p.UnicodeType, 0),
        4: ('fee', p.UVarintType, 0),
    }

    def __init__(
        self,
        namespace: str = None,
        parent: str = None,
        sink: str = None,
        fee: int = None
    ) -> None:
        self.namespace = namespace
        self.parent = parent
        self.sink = sink
        self.fee = fee
