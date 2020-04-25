from abc import abstractmethod, ABC
from os import fsync
import sys


class Reader(ABC):

    @abstractmethod
    def read(self):
        """This method shall be implemented."""


class StringReader(Reader):

    def __init__(self, input_string):
        self._char_iterator = self._get_char(input_string)

    def read(self):
        return self._char_iterator

    @staticmethod
    def _get_char(string):
        for ch in string:
            yield ch


class FileReader(Reader):

    def __init__(self, path):
        self._char_iterator = self._get_char_from_file(path)

    @staticmethod
    def _get_char_from_file(path):
        with open(path, 'rb') as file:
            while True:
                char = file.read(1)
                if char:
                    yield char
                else:
                    break

    def read(self):
        return self._char_iterator


class ConsoleReader(Reader):

    def __init__(self):
        self._char_iterator = self._get_char(input("Provide text to encode: "))

    def read(self):
        return self._char_iterator

    @staticmethod
    def _get_char(string):
        for ch in string:
            yield ch


class Writer(ABC):

    def write(self, _input):
        """This method shall be implemented."""

    def finish(self):
        """This method should be implemented if any action needed."""


class StringWriter(Writer):

    def __init__(self):
        self._output = []

    def write(self, _input):
        self._output.append(_input)

    def get(self):
        return ''.join(self._output)


class FileWriter(Writer):

    def __init__(self, path):
        self._file = open(path, 'w')

    def write(self, _input):
        self._file.write(_input)
        self._file.flush()
        fsync(self._file.fileno())

    def finish(self):
        self._file.close()


class ConsoleWriter(Writer):

    @staticmethod
    def write(_input):
        sys.stdout.write(_input)
        sys.stdout.flush()
