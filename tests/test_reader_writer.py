from mock import patch, mock_open, MagicMock
import pytest

from .._reader_writer import StringReader, StringWriter, FileReader, FileWriter, ConsoleReader, ConsoleWriter


class TestStringReader:

    def test_string_read_returns_correct_content(self):

        _string = StringReader('dude!')

        read_text = ''
        for s in _string.read():
            read_text += s

        assert read_text == 'dude!'


class TestStringWriter:

    def test_string_get_returns_correct_content(self):

        writer = StringWriter()
        writer.write('wow')
        wrote_text = writer.get()
        assert wrote_text == 'wow'


class TestFileReader:

    @pytest.fixture()
    def file_mock_set(self):
        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            f = self.open_mock.return_value
            f.read.side_effect = ['d', 'u', 'd', 'e', ' ', 'l', 'o', 'l', None]
            yield

    def test_file_read_returns_correct_content(self, file_mock_set):

        file = FileReader('path')
        read_text = ''
        for r in file.read():
            read_text += r

        assert read_text == 'dude lol'


class TestFileWriter:

    @pytest.fixture()
    def file_mock_set(self):
        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            f = self.open_mock.return_value
            f.fileno.return_value = int(1)
            with patch('os.fsync', MagicMock(return_value=None)):
                yield

    def test_file_write_is_called_with_correct_content(self, file_mock_set):

        file = FileWriter('path')
        file.write('a')

        self.open_mock.return_value.write.assert_called_once_with('a')


class TestConsoleReader:

    @pytest.fixture()
    def console_mock_set(self):
        with patch('builtins.input', lambda _: 'yep!'):
            yield

    def test_console_reader_returns_correct_content(self, console_mock_set):

        console = ConsoleReader()
        read_console = ''
        for c in console.read():
            read_console += c

        assert read_console == 'yep!'


class TestConsoleWriter:

    def test_console_write_is_called_with_correct_content(self, capsys):

        console_out = ConsoleWriter()
        console_out.write('A')

        out, _ = capsys.readouterr()

        assert out == 'A'