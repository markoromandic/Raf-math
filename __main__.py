from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter


def main():
    while True:
        try:
            text = input('rafmath: ')
        except (EOFError, KeyboardInterrupt):
            break
        if text == 'exit':
            exit('Goodbye')
        if not text:
            continue
        text += ' '
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
