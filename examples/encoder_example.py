from _encoder import Encoder
from _reader_writer import StringReader, FileWriter, ConsoleWriter, StringWriter
from _coder import Cesar, ScalarEncryptionKey

e = Encoder(StringReader('dude lol'), FileWriter(r'D:\new_one.txt'), Cesar(ScalarEncryptionKey(2)))
e.encode()

e = Encoder(StringReader('dude lol'), ConsoleWriter(), Cesar(ScalarEncryptionKey(2)))
e.encode()

e = Encoder(StringReader('dude lol'), StringWriter(), Cesar(ScalarEncryptionKey(2)))
print(e.encode().get())
