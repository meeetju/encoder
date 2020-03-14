from abc import abstractmethod, ABC


class Coder(ABC):

    @abstractmethod
    def encode_char(self, char):
        pass # pragma: no cover


class Cesar(Coder):

    MIN_ASCII_VALUE = 0
    MAX_ASCII_VALUE = 127

    def __init__(self, key=0):
        self._cesar_key = self._normalize_key_if_printables_range_exceeded(key)

    def _normalize_key_if_printables_range_exceeded(self, cesar_key):
        normalized_key = cesar_key
        if abs(cesar_key) > self.MAX_ASCII_VALUE:
            normalized_key = int((abs(cesar_key) % self.MAX_ASCII_VALUE)*(cesar_key/abs(cesar_key)))
        return normalized_key

    def encode_char(self, _char):
        return chr(self._get_new_ascii_code(_char))

    def _get_new_ascii_code(self, _char):
        current_code = ord(_char)
        new_code = current_code + self._cesar_key
        return self._rollover_key_if_printable_range_exceeded(new_code)

    def _rollover_key_if_printable_range_exceeded(self, code):
        new_code = code
        if code > self.MAX_ASCII_VALUE:
            new_code = code - self.MAX_ASCII_VALUE - 1
        return new_code


class Xor(Coder):

    def __init__(self, key=0):
        self._xor_key = key

    def encode_char(self, _char):
        return self._change_char_by_xor_key(_char)

    def _change_char_by_xor_key(self, _char):
        return chr(ord(_char) ^ self._xor_key)
