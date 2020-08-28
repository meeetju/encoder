"""Encode input text into convenient output."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC
from argparse import ArgumentParser
import logging

from text_encoder._codes import Cesar, Xor, ScalarEncryptionKey, IterableEncryptionKey
from text_encoder._readers_writers import StringReader, FileWriter, FileReader, ConsoleReader, ConsoleWriter
from text_encoder._encoders import Encoder, HeadedEncoder, NullCoder
from text_encoder._encoding_process import EncodingDoneObservable

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class BaseParser(ABC):

    """Parser interface."""

    @abstractmethod
    def get_reader(self):
        """Get selected text reader."""

    @abstractmethod
    def get_writer(self, subject):
        """Get selected text writer."""

    @abstractmethod
    def get_coder(self):
        """Get selected text coder."""

    @abstractmethod
    def is_headed(self):
        """Is text headed."""


class ParseConsoleArguments(BaseParser):

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

    def get_writer(self, subject):
        """Get selected text writer."""
        if self._arguments.out_file:
            file_writer = FileWriter(self._arguments.out_file)
            subject.register_observer(file_writer)
            return file_writer
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


class CmdEncoderFactory(object):

    """Command line Encoder factory."""

    def __init__(self, parser, encoding_done_subject=None):
        self._reader = parser.get_reader()
        self._writer = parser.get_writer(encoding_done_subject)
        self._coder = parser.get_coder()
        self._is_headed = parser.is_headed()

    def get_encoder(self):
        """Get appropriate encoder."""
        if self._is_headed:

            is_end_of_header = lambda x: x == '\n'

            header_encoder = NullCoder(self._reader, self._writer)
            body_encoder = Encoder(self._reader, self._writer, self._coder)
            return HeadedEncoder(header_encoder, body_encoder, is_end_of_header)

        return Encoder(self._reader, self._writer, self._coder)


def main():

    """Console for text Encoder."""
    arg_parser = ArgumentParser()
    parser = ParseConsoleArguments(arg_parser)

    encoding_done_subject = EncodingDoneObservable()

    CmdEncoderFactory(parser, encoding_done_subject).get_encoder().encode()

    encoding_done_subject.notify_observers()


if __name__ == '__main__':
    main()  # pragma no cover
