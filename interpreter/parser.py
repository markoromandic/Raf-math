from .lexer import *

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
variables = {}
firstToken = True


class AST(object):
    pass


class UnOp(AST):
    def __init__(self, op, value):
        self.token = self.op = op
        self.value = value


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Boolean(AST):
    def __init__(self, op, left, right):
        self.token = self.op = op
        self.left = left
        self.right = right
        self.valueNumber = left


class Variable(AST):
    def __init__(self, op):
        global variables
        self.token = self.op = op
        self.name = op.value
        if self.name in variables:
            self.value = variables[self.name]
        else:
            raise Exception('Variable not found')


class Variable_Set(AST):
    def __init__(self, op, value):
        global variables
        self.token = self.op = op
        self.name = self.token.value
        self.value = value


class Func(AST):
    def __init__(self, op, value):
        self.token = self.op = op
        self.value = value


class Constants(AST):
    def __init__(self, op):
        self.token = self.op = op


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        global firstToken
        if not firstToken and token_type == VARIABLE_SET:
            self.error()
        else:
            firstToken = False
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnOp(op=token, value=self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnOp(op=token, value=self.factor())
            return node
        elif token.type == LOG:
            self.eat(LOG)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == SQRT:
            self.eat(SQRT)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == POW:
            self.eat(POW)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == SIN:
            self.eat(SIN)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == COS:
            self.eat(COS)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == TAN:
            self.eat(TAN)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == CTG:
            self.eat(CTG)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == TRUE:
            self.eat(TRUE)
            return Bool(token)
        elif token.type == FALSE:
            self.eat(FALSE)
            return Bool(token)
        elif token.type == VARIABLE:
            self.eat(VARIABLE)
            return Variable(op=token)
        elif token.type == VARIABLE_SET:
            global variables
            self.eat(VARIABLE_SET)
            if self.current_token.type == EQ:
                self.eat(EQ)
                node = self.expr()
            elif self.current_token.type == PLUS_EQUALS:
                self.eat(PLUS_EQUALS)
                node = self.expr()
                node.value = node.value + variables[token.value]
            elif self.current_token.type == MINUS_EQUALS:
                self.eat(MINUS_EQUALS)
                node = self.expr()
                node.value = variables[token.value] - node.value
            elif self.current_token.type == MUL_EQUALS:
                self.eat(MUL_EQUALS)
                node = self.expr()
                node.value = node.value * variables[token.value]
            elif self.current_token.type == DIV_EQUALS:
                self.eat(DIV_EQUALS)
                node = self.expr()
                if isinstance(variables[token.value], int) and isinstance(node.value, int):
                    node.value = variables[token.value] // node.value
                else:
                    node.value = variables[token.value] / node.value

            return Variable_Set(op=token, value=node)
        elif token.type == PI:
            self.eat(PI)
            return Constants(op=token)
        elif token.type == E_C:
            self.eat(E_C)
            return Constants(op=token)
        elif token.type == DEG:
            self.eat(DEG)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == RAD:
            self.eat(RAD)
            self.eat(LPAREN)
            node = Func(op=token, value=self.expr())
            self.eat(RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        token = self.current_token

        if token.type == HIGHER:
            self.eat(HIGHER)
            node = Boolean(op=token, left=node, right=self.expr())
        elif token.type == LOWER:
            self.eat(LOWER)
            node = Boolean(op=token, left=node, right=self.expr())
        elif token.type == LOWER_EQ:
            self.eat(LOWER_EQ)
            node = Boolean(op=token, left=node, right=self.expr())
        elif token.type == HIGHER_EQ:
            self.eat(HIGHER_EQ)
            node = Boolean(op=token, left=node, right=self.expr())
        elif token.type == EQ_EQ:
            self.eat(EQ_EQ)
            node = Boolean(op=token, left=node, right=self.expr())
        elif token.type == LEFT_SHIFT:
            self.eat(LEFT_SHIFT)
            node = BinOp(op=token, left=node, right=self.expr())
        elif token.type == RIGHT_SHIFT:
            self.eat(RIGHT_SHIFT)
            node = BinOp(op=token, left=node, right=self.expr())

        return node

    def parse(self):
        global firstToken
        firstToken = True
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return node
