# Automatically generated by pb2py
from .. import protobuf as p
if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None
from .NEMCosignatoryModification import NEMCosignatoryModification


class NEMAggregateModification(p.MessageType):
    FIELDS = {
        1: ('modifications', NEMCosignatoryModification, p.FLAG_REPEATED),
        2: ('relative_change', p.SVarintType, 0),
    }

    def __init__(
        self,
        modifications: List[NEMCosignatoryModification] = None,
        relative_change: int = None
    ) -> None:
        self.modifications = modifications if modifications is not None else []
        self.relative_change = relative_change
