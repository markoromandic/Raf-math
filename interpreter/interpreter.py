from .lexer import PLUS, MINUS, MUL, DIV, \
    LOG, SIN, COS, TAN, CTG, SQRT, POW, LOWER, HIGHER, \
    HIGHER_EQ, LOWER_EQ, EQ_EQ, TRUE, FALSE, MOD, LEFT_SHIFT,\
    RIGHT_SHIFT, PI, E_C, DEG, RAD
from interpreter.parser import variables
import math

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            if isinstance(self.visit(node.left), int) and isinstance(self.visit(node.right), int):
                return self.visit(node.left) // self.visit(node.right)
            elif isinstance(self.visit(node.left), float) or isinstance(self.visit(node.right), float):
                return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == LEFT_SHIFT:
            return self.visit(node.left) << self.visit(node.right)
        elif node.op.type == RIGHT_SHIFT:
            return self.visit(node.left) >> self.visit(node.right)

    def visit_Constants(self, node):
        if node.op.type == PI:
            return math.pi
        elif node.op.type == E_C:
            return math.e

    def visit_UnOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.value)
        elif node.op.type == MINUS:
            return self.visit(node.value) * (-1)

    def visit_Func(self, node):
        if node.op.type == POW:
            if isinstance(self.visit(node.value), float):
                return math.pow(self.visit(node.value), 2)
            else:
                return int(math.pow(self.visit(node.value), 2))
        elif node.op.type == SQRT:
            if isinstance(self.visit(node.value), float):
                return math.sqrt(self.visit(node.value))
            else:
                return int(math.sqrt(self.visit(node.value)))
        elif node.op.type == LOG:
            if isinstance(self.visit(node.value), float):
                return math.log10(self.visit(node.value))
            else:
                return int(math.log10(self.visit(node.value)))
        elif node.op.type == SIN:
            if isinstance(self.visit(node.value), float):
                return math.sin(self.visit(node.value))
            else:
                return int(math.sin(self.visit(node.value)))
        elif node.op.type == COS:
            if isinstance(self.visit(node.value), float):
                return math.cos(self.visit(node.value))
            else:
                return int(math.cos(self.visit(node.value)))
        elif node.op.type == TAN:
            if isinstance(self.visit(node.value), float):
                return math.tan(self.visit(node.value))
            else:
                return int(math.tan(self.visit(node.value)))
        elif node.op.type == CTG:
            if isinstance(self.visit(node.value), float):
                return 1/math.tan(self.visit(node.value))
            else:
                return int(1/math.tan(self.visit(node.value)))
        elif node.op.type == RAD:
            if isinstance(self.visit(node.value), float):
                return math.radians(self.visit(node.value))
            else:
                return int(math.radians(self.visit(node.value)))
        elif node.op.type == DEG:
            if isinstance(self.visit(node.value), float):
                return math.degrees(self.visit(node.value))
            else:
                return int(math.degrees(self.visit(node.value)))

    def visit_Boolean(self, node):
        global checkBoolean
        global changedBoolean
        checkBoolean = True
        if node.op.type == HIGHER:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not left > right:
                changedBoolean = False
            return left
        elif node.op.type == LOWER:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not left < right:
                changedBoolean = False
            return left
        elif node.op.type == LOWER_EQ:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not left <= right:
                changedBoolean = False
            return left
        elif node.op.type == HIGHER_EQ:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not left >= right:
                changedBoolean = False
            return left
        elif node.op.type == EQ_EQ:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not left == right:
                changedBoolean = False
            return left

    def visit_Num(self, node):
        return node.value

    def visit_Variable(self, node):
        return node.value

    def visit_Variable_Set(self, node):
        variables[node.name] = self.visit(node.value)
        return variables[node.name]

    def visit_Bool(self, node):
        if node.value == TRUE:
            return True
        elif node.value == FALSE:
            return False

    def interpret(self):
        tree = self.parser.parse()
        global checkBoolean
        global changedBoolean
        checkBoolean = False
        changedBoolean = True
        result = self.visit(tree)

        if checkBoolean:
            return changedBoolean
        else:
            if isinstance(result, float):
                return round(result, 3)
            else:
                return result
