# Automatically generated by pb2py
from .. import protobuf as p
if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None
from .LiskTransactionCommon import LiskTransactionCommon


class LiskSignTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 116
    FIELDS = {
        1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
        2: ('transaction', LiskTransactionCommon, 0),
    }

    def __init__(
        self,
        address_n: List[int] = None,
        transaction: LiskTransactionCommon = None
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.transaction = transaction
