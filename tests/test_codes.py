import pytest

from .._coder import Coder, Cesar, Xor, IterableEncryptionKey, ScalarEncryptionKey


class ChildCoder(Coder):

    def __init__(self, key):
        super(ChildCoder, self).__init__(key)  # pragma: no cover


class TestChildCoder:

    def test_exception_raised_if_encode_letter_not_implemented(self):

        expected_fault_description = "Can't instantiate abstract class ChildCoder with " \
                                     "abstract methods encode_char"

        with pytest.raises(TypeError) as error:
            ChildCoder(ScalarEncryptionKey(3))

        assert expected_fault_description in error.value.args


class TestCesar:

    def test_cesar_encodes_printables_properly_with_positive_key(self):
        cesar = Cesar(ScalarEncryptionKey(3))
        result = cesar.encode_char('a')
        assert result == 'd'

    def test_cesar_encodes_printables_properly_with_negative_key(self):
        cesar = Cesar(ScalarEncryptionKey(-3))
        result = cesar.encode_char('a')
        assert result == '^'

    def test_cesar_encodes_printables_properly_with_positive_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(7))
        result = cesar.encode_char('z')
        assert result == '\x01'

    def test_cesar_encodes_printables_properly_with_positive_multiple_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(257))
        result = cesar.encode_char('z')
        assert result == '{'

    def test_cesar_encodes_printables_properly_with_negative_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(-6))
        result = cesar.encode_char('&')
        assert result == ' '

    def test_cesar_encodes_printables_properly_with_negative_multiple_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(-257))
        result = cesar.encode_char('&')
        assert result == '%'


class TestXor:

    def test_xor_encodes_pritable_properly(self):
        xor = Xor(ScalarEncryptionKey(3))
        result = xor.encode_char('a')
        assert result == 'b'


class TestIterableEncryptionKey:

    def test_iterator_is_looped(self):
        i = IterableEncryptionKey([1, 2, 3])
        assert i.get() == 1
        assert i.get() == 2
        assert i.get() == 3
        assert i.get() == 1


class TestScalarEncryptionKey:

    def test_key_is_converted_to_int(self):
        k = ScalarEncryptionKey('1')
        assert k.get() == 49

    def test_key_stays_int(self):
        k = ScalarEncryptionKey(1)
        assert k.get() == 1
