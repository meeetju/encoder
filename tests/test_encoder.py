"""Test encoder."""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use

from mock import patch, mock_open, MagicMock, call
import pytest

from text_encoder._coder import Cesar, Xor, ScalarEncryptionKey
from text_encoder._encoder import Encoder, HeadedTextEncoder, NullEncoder, main
from text_encoder._reader_writer import StringReader, StringWriter, FileReader, FileWriter


class TestEncoder:

    """Test Encoder."""

    @pytest.fixture()
    def file_mock_set(self):
        # pylint: disable=attribute-defined-outside-init

        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            file_ = self.open_mock.return_value
            file_.read.side_effect = ['d', 'u', 'd', 'e', ' ', 'l', 'o', 'l', None]
            file_.fileno.return_value = int(1)
            with patch('os.fsync', MagicMock(return_value=None)):
                yield

    def test_string_is_cesar_encoded_to_string(self):

        encoder = Encoder(StringReader('dude lol'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
        result_string = encoder.encode().get()

        assert result_string == 'fwfg"nqn'

    def test_file_is_cesar_encoded_to_string(self, file_mock_set):
        # pylint: disable=unused-argument

        encoder = Encoder(FileReader('dude lol'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
        result_string = encoder.encode().get()

        assert result_string == 'fwfg"nqn'

    def test_string_is_cesar_encoded_to_file(self, file_mock_set):
        # pylint: disable=unused-argument

        encoder = Encoder(StringReader('dude'),
                          FileWriter('C:\\destination.txt'),
                          Cesar(ScalarEncryptionKey(2)))
        encoder.encode()

        calls = [call('f'), call('w'), call('f'), call('g')]

        self.open_mock.return_value.write.assert_has_calls(calls)
        self.open_mock.return_value.close.assert_called_once()

    def test_string_is_xor_encoded_to_string(self):

        encoder = Encoder(StringReader('dude lol'), StringWriter(), Xor(ScalarEncryptionKey(3)))
        result_string = encoder.encode().get()

        assert result_string == 'gvgf#olo'

    def test_header_is_not_encoded(self):

        reader = StringReader('some header \n dude lol')
        writer = StringWriter()
        coder = Xor(ScalarEncryptionKey(3))

        header_encoder = NullEncoder(reader, writer)
        body_encoder = Encoder(reader, writer, coder)

        encoder = HeadedTextEncoder(header_encoder, body_encoder)
        result_string = encoder.encode().get()

        assert result_string == 'some header \n#gvgf#olo'


class TestMain:

    """Test encoder console."""

    @pytest.fixture()
    def sys_argv_mock_set(self):
        with patch('sys.argv',
                   ['main', '--in_string=this works', '--out_console', '--cesar', '--key=1']):
            yield

    def test_main_key(self, sys_argv_mock_set, capsys):
        # pylint: disable=unused-argument

        main()
        out, _ = capsys.readouterr()

        assert out == "uijt!xpslt"

    @pytest.fixture()
    def sys_argv_mock_set_keys_int(self):
        with patch('sys.argv',
                   ['main', '--in_string=this works', '--out_console',
                    '--cesar', '--keys_int=1,1,1']):
            yield

    def test_main_keys_int(self, sys_argv_mock_set_keys_int, capsys):
        # pylint: disable=unused-argument

        main()
        out, _ = capsys.readouterr()

        assert out == "uijt!xpslt"

    @pytest.fixture()
    def sys_argv_mock_set_key_text(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--out_console', '--cesar', '--key_text=abc']):
            yield

    def test_main_key_text(self, sys_argv_mock_set_key_text, capsys):
        # pylint: disable=unused-argument

        main()
        out, _ = capsys.readouterr()

        assert out == "BDF"

    @pytest.fixture()
    def sys_argv_mock_set_no_reader(self):
        with patch('sys.argv',
                   ['main', '--out_console', '--cesar', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_input_provided(self, sys_argv_mock_set_no_reader):
        # pylint: disable=unused-argument

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No reader provided.' in error.value.args

    @pytest.fixture()
    def sys_argv_mock_set_no_writer(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--cesar', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_output_provided(self, sys_argv_mock_set_no_writer):
        # pylint: disable=unused-argument

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No writer provided.' in error.value.args

    @pytest.fixture()
    def sys_argv_mock_set_no_coder(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--out_console', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_coder_provided(self, sys_argv_mock_set_no_coder):
        # pylint: disable=unused-argument

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No coder provided.' in error.value.args

    @pytest.fixture()
    def sys_argv_mock_set_no_key(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--out_console', '--cesar']):
            yield

    def test_runtime_error_raised_if_no_key_provided(self, sys_argv_mock_set_no_key):
        # pylint: disable=unused-argument

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No key nor key_vector provided.' in error.value.args