from abc import abstractmethod, ABC


class Coder(ABC):

    @abstractmethod
    def encode_char(self, char):
        """This method shall be implemented."""


class Cesar(Coder):

    MIN_ASCII_VALUE = 0
    MAX_ASCII_VALUE = 127

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
            normalized_key = int((abs(cesar_key) % (self.MAX_ASCII_VALUE + 1))*(cesar_key/abs(cesar_key)))
        if normalized_key < 0:
            normalized_key = self.MAX_ASCII_VALUE + 1 + normalized_key
        return normalized_key


class Xor(Coder):

    def __init__(self, key):
        self._xor_key = key

    def encode_char(self, _char):
        return self._change_char_by_xor_key(_char)

    def _change_char_by_xor_key(self, _char):
        return chr(ord(_char) ^ self._xor_key.get())


class ScalarEncryptionKey:

    """Scalar encryption key."""

    def __init__(self, key):
        self._initial_key = key

    def get(self):
        """Get encryption key in int format."""
        return self._get_in_int_format(self._initial_key)

    @staticmethod
    def _get_in_int_format(key):
        if isinstance(key, int):
            return key
        else:
            return ord(key)


class IterableEncryptionKey(ScalarEncryptionKey):

    """Iterable Encryption Key."""

    def __init__(self, key):
        self._initial_key = key
        self._key_iterator = self._get_next_key()

    def _get_next_key(self):
        for k in self._initial_key:
            yield self._get_in_int_format(k)

    def get(self):
        """Get encryption key in int format."""
        try:
            return self._key_iterator.__next__()
        except StopIteration:
            self._key_iterator = self._get_next_key()
            return self._key_iterator.__next__()

