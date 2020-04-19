from abc import abstractmethod, ABC


class Reader(ABC):

    @abstractmethod
    def read(self):
        """This method shall be implemented."""


class Writer(ABC):

    def __init__(self):
        self._output = []

    def write(self, _input):
        self._output.append(_input)

    @abstractmethod
    def get(self):
        pass # pragma: no cover


class StringReader(Reader):

    def __init__(self, input_string):
        self._string = input_string


    def read(self):
        return self._get_char().__

    def _get_char(self):
        for ch in self._string:
            yield ch


class FileReader(Reader):

    def __init__(self, path):
        super(FileReader, self).__init__(self._get_file_content(path))

    @staticmethod
    def _get_file_content(path):
        with open(path, 'r') as file:
            return file.read()

    def read(self):
        for char in self._input:
            yield char


class ConsoleReader(Reader):

    def __init__(self):
        super(ConsoleReader, self).__init__(input("Provide text to encode: "))


class StringWriter(Writer):

    def get(self):
        return ''.join(self._output)


class FileWriter(Writer):

    def __init__(self, path):
        self.path = path
        self._output = []

    def write(self, _input):
        self._output.append(_input)

    def get(self):
        with open(self.path, 'w') as file:
            file.write(''.join(self._output))


class ConsoleWriter(Writer):

    def get(self):
        print(''.join(self._output))