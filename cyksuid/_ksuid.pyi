import functools
from datetime import datetime
from typing import Any, Callable, Optional, Type, TypeVar, overload

from cyksuid import hints

# Constants
BYTE_LENGTH: int
STRING_ENCODED_LENGTH: int
EMPTY_BYTES: hints.Bytes
MAX_ENCODED: hints.Bytes

# Type variable for self-referential types
SelfT = TypeVar("SelfT", bound="Ksuid")

@functools.total_ordering
class Ksuid:
    """KSUIDs are 20-byte identifiers containing a 4-byte timestamp and 16-byte random payload."""

    BASE62_LENGTH: int
    PAYLOAD_LENGTH_IN_BYTES: int
    TIMESTAMP_LENGTH_IN_BYTES: int

    @overload
    def __init__(self) -> None:
        """Create a new KSUID with the current timestamp and a generated random payload."""

    @overload
    def __init__(self, raw: hints.Bytes) -> None:
        """Create a new KSUID from raw bytes."""

    @overload
    def __init__(self, timestamp: hints.IntOrFloat, payload: hints.Bytes) -> None:
        """Create a new KSUID from a specified timestamp in milliseconds and payload."""

    @overload
    def __init__(self, **kwargs: Any) -> None:
        """Create a new KSUID with additional keyword arguments."""

    @classmethod
    def from_timestamp(cls: Type[SelfT], timestamp: hints.IntOrFloat) -> SelfT:
        """Create a new KSUID with a specified timestamp and a generated random payload."""
        return cls(timestamp=timestamp, payload=os.urandom(16))

    @classmethod
    def from_payload(cls: Type[SelfT], payload: hints.Bytes) -> SelfT:
        """Create a new KSUID with the current timestamp and a specified payload."""
        return cls(timestamp=time.time(), payload=payload)

    @classmethod
    def from_timestamp_and_payload(
        cls: Type[SelfT], timestamp: hints.IntOrFloat, payload: hints.Bytes
    ) -> SelfT:
        """Create a new KSUID from a specified timestamp in milliseconds and payload."""
        return cls(timestamp=timestamp, payload=payload)

    @classmethod
    def from_bytes(cls: Type[SelfT], raw: hints.Bytes) -> SelfT:
        """Create a new KSUID from raw bytes."""
        return cls(raw=raw)

    def __bool__(self) -> bool:
        """Return True if the KSUID is not empty."""
        return self != Empty

    def __lt__(self, other: object) -> bool:
        """Compare two KSUIDs based on their timestamps and payloads."""
        if not isinstance(other, Ksuid):
            return NotImplemented
        return (self.timestamp_millis, self.payload) < (other.timestamp_millis, other.payload)

    def __eq__(self, other: object) -> bool:
        """Check if two KSUIDs are equal."""
        if not isinstance(other, Ksuid):
            return NotImplemented
        return self.bytes == other.bytes

    def __bytes__(self) -> hints.Bytes:
        """Return the raw bytes representation of the KSUID."""
        return self.bytes

    @property
    def datetime(self) -> datetime:
        """Return the datetime representation of the KSUID's timestamp (timezone-aware)."""
        return datetime.fromtimestamp(self.timestamp)

    @property
    def timestamp_millis(self) -> int:
        """Return the timestamp in milliseconds."""
        return int(self.timestamp * 1000)

    @property
    def timestamp(self) -> float:
        """Return the timestamp in seconds."""
        return self._timestamp

    @property
    def payload(self) -> hints.Bytes:
        """Return the random payload of the KSUID."""
        return self._payload

    @property
    def bytes(self) -> hints.Bytes:
        """Return the raw bytes representation of the KSUID."""
        return self._bytes

    @property
    def hex(self) -> str:
        """Return the hexadecimal representation of the KSUID."""
        return self.bytes.hex()

    @property
    def encoded(self) -> hints.Bytes:
        """Return the Base62-encoded form of the KSUID."""
        return base62_encode(self.bytes)


class Ksuid40(Ksuid):
    """KSUID compatible with a 40-bit timestamp, at 4ms precision."""


class Ksuid48(Ksuid):
    """KSUID with a 48-bit timestamp."""


def ksuid(
    time_func: Optional[hints.TimeFunc] = None,
    rand_func: Optional[hints.RandFunc] = None,
    ksuid_cls: Optional[Type[SelfT]] = None,
) -> SelfT:
    """Factory to construct KSUID objects.

    :param time_func: Function for generating time, defaults to time.time.
    :param rand_func: Function for generating random bytes, defaults to os.urandom.
    :param ksuid_cls: Class to use for KSUID, defaults to Ksuid.
    """
    if time_func is None:
        time_func = time.time
    if rand_func is None:
        rand_func = os.urandom
    if ksuid_cls is None:
        ksuid_cls = Ksuid
    return ksuid_cls.from_timestamp(time_func())


def parse(s: hints.StrOrBytes, ksuid_cls: Optional[Type[SelfT]] = None) -> SelfT:
    """Parse a KSUID from its Base62-encoded form.

    :param s: The Base62-encoded KSUID.
    :param ksuid_cls: Class to use for KSUID, defaults to Ksuid.
    """
    if ksuid_cls is None:
        ksuid_cls = Ksuid
    return ksuid_cls.from_bytes(base62_decode(s))


# Represents a completely empty (invalid) KSUID
Empty: Ksuid = Ksuid.from_bytes(b"\x00" * 20)