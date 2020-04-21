from abc import abstractmethod, ABC


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


class StringWriter(Writer):

    def get(self):
        return ''.join(self._output)

    def write(self, _input):
        self._output.append(_input)


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