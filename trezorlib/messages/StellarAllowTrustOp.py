# Automatically generated by pb2py
from .. import protobuf as p


class StellarAllowTrustOp(p.MessageType):
    MESSAGE_WIRE_TYPE = 217
    FIELDS = {
        1: ('source_account', p.BytesType, 0),
        2: ('trusted_account', p.BytesType, 0),
        3: ('asset_type', p.UVarintType, 0),
        4: ('asset_code', p.UnicodeType, 0),
        5: ('is_authorized', p.UVarintType, 0),
    }

    def __init__(
        self,
        source_account: bytes = None,
        trusted_account: bytes = None,
        asset_type: int = None,
        asset_code: str = None,
        is_authorized: int = None
    ) -> None:
        self.source_account = source_account
        self.trusted_account = trusted_account
        self.asset_type = asset_type
        self.asset_code = asset_code
        self.is_authorized = is_authorized
