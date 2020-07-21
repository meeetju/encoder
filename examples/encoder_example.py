"""Examples"""

from text_encoder._encoder import Encoder
from text_encoder._reader_writer import StringReader, FileWriter, ConsoleWriter, StringWriter
from text_encoder._codes import Cesar, ScalarEncryptionKey

encoder = Encoder(StringReader('test me'), FileWriter(r'C:\Documents\encoding_output.txt'), Cesar(ScalarEncryptionKey(2)))
encoder.encode()
encoder.finish()

encoder = Encoder(StringReader('test me'), ConsoleWriter(), Cesar(ScalarEncryptionKey(2)))
encoder.encode()
encoder.finish()

encoder = Encoder(StringReader('test me'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
encoder.encode()
print(encoder.finish().get())
