from polymede.tokenizer import *
from polymede.ast import *
from polymede.exceptions import ParserError

class Parser:

    def __init__(self, tokens: list) -> None:
        self._pos = 0
        self._tokens = tokens
        self._root = None

    def _advance(self):
        self._pos += 1

    def _next_token(self) -> Token:
        return self._tokens[self._pos]
    
    def _is_eoq(self) -> bool:
        return self._pos >= len(self._tokens) - 1

    def _assert_eoq(self):
        if not self._is_eoq():
            raise ParserError('Expected end of query, got "%s"' % (self._next_token().type))

    def _assert(self, assertion):
        if type(assertion) == list:
            if not self._next_token().type in assertion:
                raise ParserError('Expected "%s", got "%s"' % (assertion, self._next_token().type))
        
        else:
            if self._next_token().type != assertion:
                raise ParserError('Expected "%s", got "%s"' % (assertion, self._next_token().type))

    def _parse_where(self) -> AST:
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

        self._advance()
        self._assert(STRING)
        src = self._next_token().value
        format = 'auto'

        self._advance()

        if not self._is_eoq() and self._next_token().type == R_AS:
            self._advance()
            self._assert(STRING)
            format = self._next_token().value
            self._advance()

        self._assert_eoq()
        
        return LoadCommand(src, format)


    def _parse_list(self):
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
        where = None
        fields = None
        selector = None

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
            if self._next_token().type == R_WHERE:
                where = self._parse_where()
            
        return FindCommand(selector, where, fields)

    def _parse_command_count(self):
        where = None
        selector = None

        self._advance()
        
        self._assert(STRING)
        selector = self._next_token().value
        self._advance()

        if not self._is_eoq():
            if self._next_token().type == R_WHERE:
                where = self._parse_where()
            
        return CountCommand(selector, where)
    
    def _parse_command(self) -> AST:

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
        
        cmd = self._parse_command()
        if_clause = None

        return Query(cmd, if_clause)
