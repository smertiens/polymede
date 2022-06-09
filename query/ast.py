
class AST:
    pass

class Query(AST):

    def __init__(self, command, if_clause):
        self.command = command
        self.if_clause = if_clause

class String(AST):

    def __init__(self, value):
        self.value = value

class Number(AST):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{0}'.format(self.value)

    def __repr__(self):
        return self.__str__()

class ArgumentList(AST):

    def __init__(self):
        self.children = []

class LoadCommand(AST):

    def __init__(self, src, format = 'auto'):
        self.src = src
        self.format = format

class FindCommand(AST):

    def __init__(self, selector, where, fields):
        self.selector = selector
        self.where = where
        self.fields = fields

class CountCommand(AST):

    def __init__(self, selector, where):
        self.selector = selector
        self.where = where

class Where(AST):

    def __init__(self, lval, op, rval):
        self.lval = lval
        self.op = op
        self.rval = rval

