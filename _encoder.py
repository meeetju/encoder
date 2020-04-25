from argparse import ArgumentParser

from _coder import Cesar, Xor, ScalarEncryptionKey, IterableEncryptionKey
from _reader_writer import StringWriter, StringReader, FileWriter, FileReader, ConsoleReader, ConsoleWriter


class Encoder:

    def __init__(self, reader, writer, coder):
        self._reader = reader
        self._writer = writer
        self._coder = coder

    def encode(self):
        for char in self._reader.read():
            encoded = self._coder.encode_char(char)
            self._writer.write(encoded)

        self._writer.finish()

        if self._writer_has_a_getter():
            return self._writer

    def _writer_has_a_getter(self):
        return getattr(self._writer, "get", False)


class ArgParser(ArgumentParser):

    def __init__(self):
        super(ArgParser, self).__init__()
        self.add_argument('--in_string', type=type(''), default=None, help='Input string')
        self.add_argument('--in_file', type=type(''), default=None, help='Input file path')
        self.add_argument('--in_console', action='store_true', help='Console input')
        self.add_argument('--out_string', action='store_true', help='Return string')
        self.add_argument('--out_file', type=type(''), default=None, help='Output file path')
        self.add_argument('--out_console', action='store_true', help='Console output')
        self.add_argument('--cesar', action='store_true', help='Select the Cesar code')
        self.add_argument('--xor', action='store_true', help='Select the Xor code')
        self.add_argument('--key', type=int, default=0, help='Key to selected code')
        self.add_argument('--keys_int', type=str, default=0, help='Vector of coma-separated int keys to selected code')
        self.add_argument('--key_text', type=str, default=0, help='String of keys to selected code')
        self.arguments = self.parse_args()

    def get_reader(self):
        if self.arguments.in_string:
            return StringReader(self.arguments.in_string)
        elif self.arguments.in_file:
            return FileReader(self.arguments.in_file)
        elif self.arguments.in_console:
            return ConsoleReader()
        else:
            raise RuntimeError('No input provided.')

    def get_writer(self):
        if self.arguments.out_string:
            return StringWriter()
        elif self.arguments.out_file:
            return FileWriter(self.arguments.out_file)
        elif self.arguments.out_console:
            return ConsoleWriter()
        else:
            raise RuntimeError('No output provided.')

    def get_coder(self):
        if self.arguments.cesar:
            return Cesar(self._get_key())
        elif self.arguments.xor:
            return Xor(self._get_key())
        else:
            raise RuntimeError('No coder provided.')

    def _get_key(self):
        if self.arguments.key:
            return ScalarEncryptionKey(self.arguments.key)
        elif self.arguments.keys_int:
            return IterableEncryptionKey([int(i) for i in self.arguments.keys_int.split(',')])
        elif self.arguments.key_text:
            return IterableEncryptionKey(self.arguments.key_text)
        else:
            raise RuntimeError('No key nor key_vector provided.')


def main():

    parser = ArgParser()
    reader = parser.get_reader()
    writer = parser.get_writer()
    coder = parser.get_coder()

    encoder = Encoder(reader, writer, coder)
    encoder.encode()


if __name__ == '__main__':
    main()