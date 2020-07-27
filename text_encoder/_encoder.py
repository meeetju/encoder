"""Encode input text into convenient output."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC
from argparse import ArgumentParser
import logging
import time

from ._codes import Cesar, Xor, ScalarEncryptionKey, IterableEncryptionKey
from ._reader_writer import StringReader, FileWriter, FileReader, ConsoleReader, ConsoleWriter

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def time_it(original_function):
    """Log time of executed function.

    :param original_function: function which execution time is measured
    :type original_function: function
    :return: wrapper
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        t1 = time.time()
        original_function(*args, **kwargs)
        t2 = time.time()
        logging.info('{} complete in {:.2f} seconds.'.format(original_function.__name__, t2 - t1))

    return wrapper


class BaseEncoder(ABC):

    """Encoder interface."""

    @abstractmethod
    def encode(self, stop_predicate):
        """This method shall be implemented."""


class Encoder(BaseEncoder):

    """Encode input from reader."""

    def __init__(self, reader, writer, coder):
        self._reader = reader
        self._writer = writer
        self._coder = coder

    def _encode(self, char):
        return self._coder.encode_char(char)

    @time_it
    def encode(self, stop_predicate=lambda x: False):
        """Encode input from reader.

        :param stop_predicate: predicate
        :type stop_predicate: function

        """
        for char in self._reader.read():
            encoded_char = self._encode(char)
            self._writer.write(encoded_char)
            if stop_predicate(char):
                return


class NullCoder(BaseEncoder):

    """Rewrite reader input to output."""

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    def encode(self,  stop_predicate=lambda x: False):
        """Rewrite reader input to output until stop condition is met.

        :param stop_predicate: predicate
        :type stop_predicate: function

        """
        for char in self._reader.read():
            self._writer.write(char)
            if stop_predicate(char):
                return


class HeadedEncoder(BaseEncoder):

    """Encode body, leaving header not encoded."""

    def __init__(self, header_encoder, body_encoder, is_end_of_header_predicate):
        self._header_encoder = header_encoder
        self._body_encoder = body_encoder
        self._is_end_of_header_predicate = is_end_of_header_predicate
        self._is_end_of_header_reached = False

    def _is_end_of_header(self, char):
        self._is_end_of_header_reached = self._is_end_of_header_predicate(char)
        return self._is_end_of_header_reached

    def encode(self, stop_predicate=lambda x: False):
        """Encode body."""
        self._header_encoder.encode(lambda x: stop_predicate(x) or self._is_end_of_header(x))
        if self._is_end_of_header_reached:
            self._body_encoder.encode(stop_predicate)


class EncodingState:

    """Encoding states."""

    START = 1
    END = 2


class EncodingObserver:

    """Encoding observer."""

    def __init__(self):
        self._finish_functions = []

    def update(self, state):
        """Update with new state

        :param state: state of encoding
        :type state: int

        """
        if state == EncodingState.END:
            for func in self._finish_functions:
                func()

    def register_finish_function(self, func):
        """Register finish function.

        :param func: finish function to be executed
        :type func: function

        """
        self._finish_functions.append(func)


class ParseConsoleArguments:

    """Parse input arguments."""

    def __init__(self, parser):
        self.parser = parser
        self.parser.add_argument('--in_string', type=type(''), default=None, help='Input string')
        self.parser.add_argument('--in_file', type=type(''), default=None, help='Input file path')
        self.parser.add_argument('--in_console', action='store_true', help='Console input')
        self.parser.add_argument('--out_file', type=type(''), default=None, help='Output file path')
        self.parser.add_argument('--out_console', action='store_true', help='Console output')
        self.parser.add_argument('--cesar', action='store_true', help='Select the Cesar code')
        self.parser.add_argument('--xor', action='store_true', help='Select the Xor code')
        self.parser.add_argument('--key', type=int, default=0, help='Key to selected code')
        self.parser.add_argument('--keys_int', type=str, default=0,
                          help='Vector of coma-separated int keys to selected code')
        self.parser.add_argument('--key_text', type=str, default=0,
                          help='String of keys to selected code')
        self.parser.add_argument('--headed', action='store_true', help='Message has header')
        self._arguments = self.parser.parse_args()

    def get_reader(self):
        """Get selected text reader."""
        if self._arguments.in_string:
            return StringReader(self._arguments.in_string)
        if self._arguments.in_file:
            return FileReader(self._arguments.in_file)
        if self._arguments.in_console:
            return ConsoleReader()
        raise RuntimeError('No reader provided.')

    def get_writer(self, observer):
        """Get selected text writer."""
        if self._arguments.out_file:
            file_writer = FileWriter(self._arguments.out_file)
            observer.register_finish_function(file_writer.finish)
            return FileWriter(self._arguments.out_file)
        if self._arguments.out_console:
            return ConsoleWriter()
        raise RuntimeError('No writer provided.')

    def get_coder(self):
        """Get selected text coder."""
        if self._arguments.cesar:
            return Cesar(self._get_key())
        if self._arguments.xor:
            return Xor(self._get_key())
        raise RuntimeError('No coder provided.')

    def _get_key(self):
        if self._arguments.key:
            return ScalarEncryptionKey(self._arguments.key)
        if self._arguments.keys_int:
            return IterableEncryptionKey([int(i) for i in self._arguments.keys_int.split(',')])
        if self._arguments.key_text:
            return IterableEncryptionKey(self._arguments.key_text)
        raise RuntimeError('No key nor key_vector provided.')

    def is_headed(self):
        """Is text headed.

        :return: is_headed
        :rtype: bool
        """
        return self._arguments.headed


def main():

    """Console for text Encoder."""
    arg_parser = ArgumentParser()
    parser = ParseConsoleArguments(arg_parser)
    encoding_observer = EncodingObserver()

    reader = parser.get_reader()
    writer = parser.get_writer(encoding_observer)

    coder = parser.get_coder()
    is_headed = parser.is_headed()

    if is_headed:

        is_end_of_header = lambda x: x == '\n'

        header_encoder = NullCoder(reader, writer)
        body_encoder = Encoder(reader, writer, coder)
        encoder = HeadedEncoder(header_encoder, body_encoder, is_end_of_header)
    else:
        encoder = Encoder(reader, writer, coder)
    encoder.encode()

    encoding_observer.update(EncodingState.END)


if __name__ == '__main__':
    main()  # pragma no cover
