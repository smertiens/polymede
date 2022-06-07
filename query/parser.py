from .tokenizer import *
from .ast import *

class ParserError(Exception):
    pass

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
        return self._pos != len(self._tokens) - 1

    def _assert_eoq(self):
        if not self._is_eoq():
            raise ParserError('Expected end of query, got "%s"' % (self._next_token().type))

    def _assert(self, assertion):
        if self._next_token().type != assertion:
            raise ParserError('Expected "%s", got "%s"' % (assertion, self._next_token().type))
        
    def _parse_command_load(self) -> AST:

        self._advance()
        self._assert(STRING)
        src = self._next_token().value
        format = 'auto'

        self._advance()

        if not self._is_eoq() and self._next_token().type == R_AS:
            self._advance
            self._assert(STRING)
            format = self._next_token().value
            self._advance

        self._assert_eoq()
        
        return LoadCommand(src, format)

    def _parse_command_find(self):
        self._advance()
        range = None
        level = 'root'
        selector = None

        if self._next_token().type == R_ALL:
            range = 'all'
        elif self._next_token().type == R_FIRST:
            range = 'first'
        elif self._next_token().type == R_LAST:
            range = 'last'
        else:
            raise ParserError('Expected "all", "first" or "last"')
        
        self._advance()

        if not self._is_eoq() and not self._next_token().type == R_WHERE:
            if self._next_token().type == R_OF:
                self._advance()
                level = 'nested'
                
            self._assert(STRING)
            selector = self._next_token().value
            self._advance()

        return FindCommand(range, level, selector)

    
    def _parse_command(self) -> AST:

        self._assert(SYMBOL)
        cmd = self._next_token().value.lower()

        if cmd == 'load':
            return self._parse_command_load()

        elif cmd == 'find':
            return self._parse_command_find()

        else:
            raise ParserError('Unknown command: "%s"' % cmd)

    def parse(self) -> AST:
        
        cmd = self._parse_command()
        if_clause = None

        return Query(cmd, if_clause)
