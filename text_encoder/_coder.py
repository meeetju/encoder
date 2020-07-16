"""Set of letter coders"""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC


def _get_in_int_format(key):
    if isinstance(key, int):
        return key
    return ord(key)


class Coder(ABC):

    """Coder interface."""

    @abstractmethod
    def encode_char(self, char):
        """This method shall be implemented."""


class Cesar(Coder):

    """Encode letter with Cesar code."""

    MIN_ASCII_VALUE = 0
    MAX_ASCII_VALUE = 127
    ASCII_TABLE_SIZE = MAX_ASCII_VALUE + 1

    def __init__(self, key):
        self._cesar_key = key

    def encode_char(self, _char):
        return chr(self._get_new_ascii_code(_char))

    def _get_new_ascii_code(self, _char):
        current_code = ord(_char)
        new_code = current_code + self._cesar_key.get()
        return self._normalize_key_if_printables_range_exceeded(new_code)

    def _normalize_key_if_printables_range_exceeded(self, cesar_key):
        normalized_key = cesar_key
        if abs(cesar_key) > self.MAX_ASCII_VALUE:
            normalized_key = int(
                (abs(cesar_key) % self.ASCII_TABLE_SIZE)*(cesar_key/abs(cesar_key)))
        if normalized_key < self.MIN_ASCII_VALUE:
            normalized_key += self.ASCII_TABLE_SIZE
        return normalized_key


class Xor(Coder):

    """Encode letter with Xor code."""

    def __init__(self, key):
        self._xor_key = key

    def encode_char(self, _char):
        return self._change_char_by_xor_key(_char)

    def _change_char_by_xor_key(self, _char):
        return chr(ord(_char) ^ self._xor_key.get())


class EncryptionKey(ABC):

    """Encryption Key Interface."""

    @abstractmethod
    def get(self):
        """This method shall be implemented."""


class ScalarEncryptionKey(EncryptionKey):

    """Scalar encryption key."""

    def __init__(self, key):
        self._initial_key = key

    def get(self):
        """Get encryption key in int format."""
        return _get_in_int_format(self._initial_key)


class IterableEncryptionKey(EncryptionKey):

    """Iterable Encryption Key."""

    def __init__(self, key):
        self._initial_key = key
        self._key_iterator = self._get_next_key()

    def _get_next_key(self):
        for k in self._initial_key:
            yield _get_in_int_format(k)

    def get(self):
        """Get encryption key in int format."""
        try:
            return self._key_iterator.__next__()
        except StopIteration:
            self._key_iterator = self._get_next_key()
            return self._key_iterator.__next__()
