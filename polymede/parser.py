from polymede.tokenizer import *
from polymede.ast import *
from polymede.exceptions import ParserError

class Parser:
    """ Parses the token-list returned from the tokenizer and creates an abstract syntax tree (AST). """

    def __init__(self, tokens: list) -> None:
        """ Create new parser instance """
        self._pos = 0
        self._tokens = tokens
        self._root = None

    def _advance(self):
        """ Move one token forward """
        self._pos += 1

    def _next_token(self) -> Token:
        """ Return the token at the current position """
        return self._tokens[self._pos]
    
    def _is_eoq(self) -> bool:
        """ Returns true if the end-of-query is reached """
        return self._pos >= len(self._tokens) - 1

    def _assert_eoq(self):
        """ Will raise an exception if the end of the query is reached """
        if not self._is_eoq():
            raise ParserError('Expected end of query, got "%s"' % (self._next_token().type))

    def _assert(self, assertion):
        """ Will raise an exception if current token ist not in the given list """
        if type(assertion) == list:
            if not self._next_token().type in assertion:
                raise ParserError('Expected "%s", got "%s"' % (assertion, self._next_token().type))
        
        else:
            if self._next_token().type != assertion:
                raise ParserError('Expected "%s", got "%s"' % (assertion, self._next_token().type))

    def _parse_where(self) -> AST:
        """ Parse a where expression """
        lval = None
        op = None
        rval = None
        
        self._advance()
        self._assert(STRING)
        lval = self._next_token().value
        self._advance()

        self._assert([COMP_EQ, COMP_LT, COMP_GT, COMP_LT_EQ, COMP_GT_EQ, COMP_NOT_EQ])
        op = self._next_token().value
        self._advance()

        rval = self._next_token().value

        return Where(lval, op, rval)
        
    def _parse_command_load(self) -> AST:
        """ Parse load command """
        self._advance()
        self._assert(STRING)
        src = self._next_token().value
        format = 'auto'

        self._advance()

        if not self._is_eoq() and self._next_token().type == AS:
            self._advance()
            self._assert(STRING)
            format = self._next_token().value
            self._advance()

        self._assert_eoq()
        
        return LoadCommand(src, format)


    def _parse_list(self):
        """ Parse list """
        self._assert(LPAR)
        self._advance()

        token = self._next_token()
        lst = []

        while token.type != RPAR:
            if token.type == EOF:
                raise ParserError('Unexpected end of list')
            elif token.type == COMMA:
                self._advance()
            else:
                lst.append(token.value)
                self._advance()
                
            token = self._next_token()
        
        self._advance()     # consume RPAR
        return lst

    def _parse_command_find(self):
        """ Parse find command """
        where = None
        fields = None
        selector = None
        sortBy = None

        self._advance()
        self._assert([STRING, LPAR])

        if self._next_token().type == LPAR:
            fields = self._parse_list()
            self._assert(IN)
            self._advance()
        
        self._assert(STRING)
        selector = self._next_token().value
        self._advance()

        if not self._is_eoq():
            if self._next_token().type == WHERE:
                where = self._parse_where()
                self._advance()

        if not self._is_eoq():
            if self._next_token().type == SYMBOL and self._next_token().value.lower()in  ('sortby', 'sort'):
                sortBy = self._parse_sort_expression()
            
        return FindCommand(selector, where, fields, sortBy)

    def _parse_sort_expression(self):
        arg1 = None
        arg2 = None

        self._advance()
        self._assert(LPAR)
        self._advance()
        self._assert([STRING, SYMBOL])

        arg1 = self._next_token().value
        self._advance()
        self._assert([COMMA, RPAR])

        if self._next_token().type == COMMA:
            # two arguments -> sortBy 
            self._advance()
            self._assert([STRING, SYMBOL])
            arg2 = self._next_token().value
            self._advance()
            return sortBy(arg1, arg2)

        else:
            # one argument -> sort
            return sort(arg1)

    def _parse_command_count(self):
        """ Parse count command """
        where = None
        selector = None

        self._advance()
        
        self._assert(STRING)
        selector = self._next_token().value
        self._advance()

        if not self._is_eoq():
            if self._next_token().type == WHERE:
                where = self._parse_where()
            
        return CountCommand(selector, where)
    
    def _parse_command(self) -> AST:
        """ Determine the main command for this query """
        self._assert(SYMBOL)
        cmd = self._next_token().value.lower()

        if cmd == 'load':
            return self._parse_command_load()

        elif cmd == 'find':
            return self._parse_command_find()

        elif cmd == 'count':
            return self._parse_command_count()

        else:
            raise ParserError('Unknown command: "%s"' % cmd)

    def parse(self) -> AST:
        """ Start parsing """
        cmd = self._parse_command()
        if_clause = None

        return Query(cmd, if_clause)
