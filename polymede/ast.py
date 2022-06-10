
class AST:
    """ Base class for AST """
    pass

class Query(AST):
    """ Root item for all parsing trees. Represents a single query. """
    def __init__(self, command, if_clause):
        self.command = command
        self.if_clause = if_clause

class String(AST):
    """ A string value """
    def __init__(self, value):
        self.value = value

class Number(AST):
    """ A numeric value (can be int or float) """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{0}'.format(self.value)

    def __repr__(self):
        return self.__str__()

class ArgumentList(AST):
    """ Represents a list """
    def __init__(self):
        self.children = []

class LoadCommand(AST):
    """ Load command """
    def __init__(self, src, format = 'auto'):
        self.src = src
        self.format = format

class FindCommand(AST):
    """ Find command """
    def __init__(self, selector, where, fields):
        self.selector = selector
        self.where = where
        self.fields = fields

class CountCommand(AST):
    """ Count command """
    def __init__(self, selector, where):
        self.selector = selector
        self.where = where

class Where(AST):
    """ A single where clause """
    def __init__(self, lval, op, rval):
        self.lval = lval
        self.op = op
        self.rval = rval