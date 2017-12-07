# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
NUMBER, VARIABLE, VARIABLE_SET, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, LOG, SIN, COS, TAN, \
CTG, SQRT, POW, LOWER, HIGHER, HIGHER_EQ, LOWER_EQ, EQ, EQ_EQ, TRUE, FALSE, PLUS_EQUALS,\
    MINUS_EQUALS, MUL_EQUALS, DIV_EQUALS, MOD, LEFT_SHIFT, RIGHT_SHIFT, PI, E_C, DEG, RAD = (
    'NUMBER', 'VARIABLE', 'VARIABLE_SET', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'LOG', \
    'SIN', 'COS', 'TG', 'CTG', 'SQRT', 'POW', '<', '>', '>=', '<=', '=', '==', 'True', 'False', '+=',\
    '-=', '*=', '/=', '%', '<<', '>>', 'PI', 'E', 'DEG', 'RAD'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        foundDot = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                foundDot = True
            result += self.current_char
            self.advance()
        if foundDot:
            return float(result)
        else:
            return int(result)

    def var(self):
        charName = ''
        while self.current_char is not None and self.current_char != '(' and self.current_char != '+' \
                and self.current_char != '-' and self.current_char != '*' and self.current_char != '/' \
                and not self.current_char.isspace() and self.current_char != '=' and self.current_char != '>' \
                and self.current_char != '<':
            charName += self.current_char
            self.advance()

        if self.current_char is not None and self.current_char.isspace():
            self.skip_whitespace()

        return charName

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            position = self.pos

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                br = self.number()
                return Token(NUMBER, br)

            if self.text[self.pos: self.pos + 2] == PLUS_EQUALS:
                self.advance()
                self.advance()
                return Token(PLUS_EQUALS, PLUS_EQUALS)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.text[self.pos: self.pos + 2] == MINUS_EQUALS:
                self.advance()
                self.advance()
                return Token(MINUS_EQUALS, MINUS_EQUALS)

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.text[self.pos: self.pos + 2] == MUL_EQUALS:
                self.advance()
                self.advance()
                return Token(MUL_EQUALS, MUL_EQUALS)

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.text[self.pos: self.pos + 2] == DIV_EQUALS:
                self.advance()
                self.advance()
                return Token(DIV_EQUALS, DIV_EQUALS)

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == MOD:
                self.advance()
                return Token(MOD, MOD)

            if self.text[self.pos: self.pos + 2] == EQ_EQ:
                self.advance()
                self.advance()
                return Token(EQ_EQ, EQ_EQ)

            if self.current_char == EQ:
                self.advance()
                return Token(EQ, EQ)

            if self.text[self.pos: self.pos + 2] == LEFT_SHIFT:
                self.advance()
                self.advance()
                return Token(LEFT_SHIFT, LEFT_SHIFT)

            if self.text[self.pos: self.pos + 2] == LOWER_EQ:
                self.advance()
                self.advance()
                return Token(LOWER_EQ, LOWER_EQ)

            if self.current_char == LOWER:
                self.advance()
                return Token(LOWER, LOWER)

            if self.text[self.pos: self.pos + 2] == RIGHT_SHIFT:
                self.advance()
                self.advance()
                return Token(RIGHT_SHIFT, RIGHT_SHIFT)

            if self.text[self.pos: self.pos + 2] == HIGHER_EQ:
                self.advance()
                self.advance()
                return Token(HIGHER_EQ, HIGHER_EQ)

            if self.current_char == HIGHER:
                self.advance()
                return Token(HIGHER, HIGHER)

            if self.text[self.pos: self.pos + 5] == SQRT + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(SQRT, SQRT)

            if self.text[self.pos: self.pos + 4] == SIN + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(SIN, SIN)

            if self.text[self.pos: self.pos + 3] == TAN + LPAREN:
                self.advance()
                self.advance()
                return Token(TAN, TAN)

            if self.text[self.pos: self.pos + 4] == POW + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(POW, POW)

            if self.text[self.pos: self.pos + 4] == COS + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(COS, COS)

            if self.text[self.pos: self.pos + 4] == CTG + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(CTG, CTG)

            if self.text[self.pos: self.pos + 4] == LOG + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(LOG, LOG)

            if self.text[self.pos: self.pos + 4] == DEG + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(DEG, DEG)

            if self.text[self.pos: self.pos + 4] == RAD + LPAREN:
                self.advance()
                self.advance()
                self.advance()
                return Token(RAD, RAD)

            if self.text[self.pos: self.pos + 4] == TRUE:
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                if self.current_char.isalpha:
                    self.pos = self.pos - 4
                    self.current_char = self.text[self.pos]
                else:
                    return Token(TRUE, TRUE)

            if self.text[self.pos: self.pos + 5] == FALSE:
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                if self.current_char.isalpha:
                    self.pos = self.pos - 5
                    self.current_char = self.text[self.pos]
                else:
                    return Token(FALSE, FALSE)

            if self.current_char.isalpha():
                charName = self.var()
                if charName == PI:
                    return Token(PI, PI)
                elif charName == E_C:
                    return Token(E_C, E_C)

                if self.current_char is None:
                    retrunToThisPos = self.pos - 1
                else:
                        retrunToThisPos = self.pos

                if self.current_char == '=':
                    self.advance()
                    if self.current_char == '=':
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE, charName)
                    else:
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE_SET, charName)
                elif self.current_char == '+':
                    self.advance()
                    if self.current_char == '=':
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE_SET, charName)
                    else:
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE, charName)
                elif self.current_char == '*':
                    self.advance()
                    if self.current_char == '=':
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE_SET, charName)
                    else:
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE, charName)
                elif self.current_char == '/':
                    self.advance()
                    if self.current_char == '=':
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE_SET, charName)
                    else:
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE, charName)
                elif self.current_char == '-':
                    self.advance()
                    if self.current_char == '=':
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE_SET, charName)
                    else:
                        self.pos = retrunToThisPos
                        self.current_char = self.text[self.pos]
                        return Token(VARIABLE, charName)
                else:
                    self.pos = retrunToThisPos
                    self.current_char = self.text[self.pos]
                    return Token(VARIABLE, charName)
            self.error()

        return Token(EOF, None)
