class GeneratorException(Exception):
    __code = 1
    __text = ''

    def __init__(self, text: str = '', code: int = 1):
        super().__init__(text)
        self.__code = code
        self.__text = text

    def code(self) -> int:
        return self.__code

    def __str__(self) -> str:
        return self.__text


class ParserException(GeneratorException):
    def __init__(self, text: str = ''):
        super().__init__(text, 2)
