import functools
from datetime import datetime
from typing import Any, Optional, Type, TypeVar

from cyksuid import hints

BYTE_LENGTH: int
STRING_ENCODED_LENGTH: int
EMPTY_BYTES: hints.Bytes
MAX_ENCODED: hints.Bytes

SelfT = TypeVar("SelfT", bound="Ksuid")

@functools.total_ordering
class Ksuid:
    """KSUIDs are 20 bytes contains 4 byte timestamp with custom epoch and 16 bytes random data."""

    BASE62_LENGTH: int
    PAYLOAD_LENGTH_IN_BYTES: int
    TIMESTAMP_LENGTH_IN_BYTES: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a new KSUID with various initialization options."""

    @classmethod
    def from_timestamp(cls: Type[SelfT], timestamp: hints.IntOrFloat) -> SelfT:
        """Create a new KSUID with specified timestamp and generated random payload."""
        
    @classmethod
    def from_bytes(cls: Type[SelfT], raw: hints.Bytes) -> SelfT:
        """Create a new KSUID from raw bytes."""

    def __bool__(self) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __bytes__(self) -> hints.Bytes: ...

    @property
    def datetime(self) -> datetime: ...
    @property
    def timestamp_millis(self) -> int: ...
    @property
    def timestamp(self) -> float: ...
    @property
    def payload(self) -> hints.Bytes: ...
    @property
    def bytes(self) -> hints.Bytes: ...
    @property
    def hex(self) -> str: ...
    @property
    def encoded(self) -> hints.Bytes: ...

class Ksuid40(Ksuid):
    """KSUID compatible with 40 bit timestamp, at 4ms precision."""

class Ksuid48(Ksuid):
    """KSUID with 48 bit timestamp."""

def ksuid(
    time_func: Optional[hints.TimeFunc] = None,
    rand_func: Optional[hints.RandFunc] = None,
    ksuid_cls: Optional[Type[SelfT]] = None,
) -> SelfT: ...

def parse(s: hints.StrOrBytes, ksuid_cls: Optional[Type[SelfT]] = None) -> SelfT: ...

Empty: Ksuid
