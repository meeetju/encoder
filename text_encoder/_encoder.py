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
    def encode(self):
        """This method shall be implemented."""

    @abstractmethod
    def finish(self):
        """This method shall be implemented."""


class Encoder(BaseEncoder):

    """Encode text."""
    # pylint: disable=inconsistent-return-statements

    def __init__(self, reader, writer, coder):
        self._reader = reader
        self._writer = writer
        self._coder = coder

    def _encode(self, char):
        return self._coder.encode_char(char)

    @time_it
    def encode(self):
        """Encode text.

        :return: text writer
        :rtype: Writer

        """
        for char in self._reader.read():
            encoded_char = self._encode(char)
            self._writer.write(encoded_char)

    def finish(self):
        """Execute writer finish actions."""
        return self._writer.finish()


class NullEncoder(BaseEncoder):

    """Rewrite input text."""

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    def encode(self, stop_predicate):
        """Encode text.

        :param stop_predicate: predicate
        :type stop_predicate: function
        :return: text writer
        :rtype: Writer

        """
        for char in self._reader.read():
            self._writer.write(char)
            if stop_predicate(char):
                break

    def finish(self):
        """Execute writer finish actions."""
        return self._writer.finish()


class HeadedTextEncoder(BaseEncoder):

    """Encode text leaving header not encoded."""

    def __init__(self, header_encoder, body_encoder):
        self._header_encoder = header_encoder
        self._body_encoder = body_encoder

    def encode(self):
        """Encode text."""
        self._header_encoder.encode(self._is_end_of_header)
        return self._body_encoder.encode()

    @staticmethod
    def _is_end_of_header(char):
        return char == '\n'

    def finish(self):
        """Execute writer finish actions."""
        return self._body_encoder.finish()


class ArgParser(ArgumentParser):

    """Parse input arguments."""

    def __init__(self):
        super(ArgParser, self).__init__()
        self.add_argument('--in_string', type=type(''), default=None, help='Input string')
        self.add_argument('--in_file', type=type(''), default=None, help='Input file path')
        self.add_argument('--in_console', action='store_true', help='Console input')
        self.add_argument('--out_file', type=type(''), default=None, help='Output file path')
        self.add_argument('--out_console', action='store_true', help='Console output')
        self.add_argument('--cesar', action='store_true', help='Select the Cesar code')
        self.add_argument('--xor', action='store_true', help='Select the Xor code')
        self.add_argument('--key', type=int, default=0, help='Key to selected code')
        self.add_argument('--keys_int', type=str, default=0,
                          help='Vector of coma-separated int keys to selected code')
        self.add_argument('--key_text', type=str, default=0,
                          help='String of keys to selected code')
        self.add_argument('--headed', action='store_true', help='Message has header')
        self._arguments = self.parse_args()

    def get_reader(self):
        """Get selected text reader."""
        if self._arguments.in_string:
            return StringReader(self._arguments.in_string)
        if self._arguments.in_file:
            return FileReader(self._arguments.in_file)
        if self._arguments.in_console:
            return ConsoleReader()
        raise RuntimeError('No reader provided.')

    def get_writer(self):
        """Get selected text writer."""
        if self._arguments.out_file:
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

    parser = ArgParser()
    reader = parser.get_reader()
    writer = parser.get_writer()
    coder = parser.get_coder()
    is_headed = parser.is_headed()

    if is_headed:
        header_encoder = NullEncoder(reader, writer)
        body_encoder = Encoder(reader, writer, coder)
        encoder = HeadedTextEncoder(header_encoder, body_encoder)
    else:
        encoder = Encoder(reader, writer, coder)
    encoder.encode()
    encoder.finish()


if __name__ == '__main__':
    main()  # pragma no cover
