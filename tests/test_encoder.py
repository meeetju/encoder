from mock import patch, mock_open
import pytest

from .._coder import Cesar, Xor, IterableEncryptionKey, ScalarEncryptionKey
from ..encoder import Encoder, main
from .._reader_writer import StringReader, StringWriter, FileReader, FileWriter


class TestEncoder:

    @pytest.fixture()
    def file_mock_set(self):
        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            self.open_mock.return_value.read.side_effect = ['d', 'u', 'd', 'e', ' ', 'l', 'o', 'l', None]
            yield

    def test_string_is_cesar_encoded_to_string(self):

        encoder = Encoder(StringReader('dude lol'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        result_string = encoder.get()
        assert result_string == 'fwfg"nqn'

    def test_file_is_cesar_encoded_to_string(self, file_mock_set):

        encoder = Encoder(FileReader('dude lol'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        result_string = encoder.get()

        assert result_string == 'fwfg"nqn'

    def test_string_is_cesar_encoded_to_file(self, file_mock_set):

        encoder = Encoder(StringReader('dude lol'), FileWriter('C:\\destination.txt'), Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        encoder.get()

        self.open_mock.return_value.write.assert_called_once_with('fwfg"nqn')

    def test_string_is_xor_encoded_to_string(self):

        encoder = Encoder(StringReader('dude lol'), StringWriter(), Xor(ScalarEncryptionKey(3)))
        encoder.encode()
        result_string = encoder.get()

        assert result_string == 'gvgf#olo'


# class TestMain:
#
#     @pytest.fixture()
#     def sys_argv_mock_set(self):
#         with patch('sys.argv', ['main', '--in_string=this works', '--out_console', '--cesar', '--key=1']):
#             yield
#
#     def test_main(self, sys_argv_mock_set, capsys):
#         main()
#         captured = capsys.readouterr()
#
#         assert captured.out == "uijt!xpslt\n"