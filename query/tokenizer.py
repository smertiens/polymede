import logging

from iniconfig import ParseError

class SyntaxError(Exception):
    pass

# Tokens
STRING, INTEGER, LIST, SYMBOL, EOF = 'STRING', 'INTEGER', 'LIST', 'SYMBOL', 'EOF',
LPAR, RPAR, COMMA, LSQRBR, RSQRBR, NEWLINE, IF = 'LPAR', 'RPAR', 'COMMA', 'LSQRBR', 'RSQRBR', 'NEWLINE', 'IF'
COMP_EQ, COMP_LT, COMP_GT, COMP_LT_EQ, COMP_GT_EQ, COMP_NOT_EQ = 'COMP_EQ', 'COMP_LT', 'COMP_GT', 'COMP_LT_EQ', \
                                                                                                  'COMP_GT_EQ', 'COMP_NOT_EQ'
R_AS, R_OF, R_ALL, R_FIRST, R_LAST, R_WHERE = 'R_AS', 'R_OF', 'R_ALL', 'R_FIRST', 'R_LAST', 'R_WHERE'
IN = 'IN'

class Token:

    type: str = None
    value: any = None

    def __init__(self, type: str, value: any = None) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return "<Token type='%s' value='%s'>" % (self.type, self.value)

    def __repr__(self) -> str:
        return str(self)

class Tokenizer:
    def __init__(self) -> None:
        self._pos = 0
        self._line = 0
        self._token = None
        self._text = ''

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def tokenize(self, text: str):
        self._text = text
        token = self.get_next_token()
        lst = []

        while token.type != EOF:
            lst.append(token)
            token = self.get_next_token()

        return lst

    def set_text(self, text):
        self._text = text

    def get_chr(self):
        try:
            return self._text[self._pos]
        except IndexError:
            return None

    def _advance(self):
        self._pos += 1

    def lookahead(self, size=1):
        try:
            return self._text[self._pos + 1:self._pos + 1 + size]
        except IndexError:
            return None

    def _skip_whitespace(self):
        while self.get_chr() is not None and self.get_chr().isspace() and self.get_chr() != '\n':
            self._advance()

    def get_raw(self, end_delim='\n'):

        raw = ''
        while self.get_chr() is not None and self.get_chr() != end_delim:
            raw += self.get_chr()
            self._advance()

        return raw

    def skip_until(self, delim='\n'):
        while self.get_chr() is not None and self.get_chr() not in delim:
            self._advance()

    def get_next_token(self):
        """
        Retrieves the next token from the text stream.

        :return: The next token
        :rtype: Token
        """
        token = None
        advance = 0

        self._skip_whitespace()
        
        if self.get_chr() is None:
            return Token(EOF)
        
        if self.get_chr() == 'a' and self.lookahead() == 's':
            token = Token(R_AS)
            advance = 2

        elif self.get_chr() == 'a' and self.lookahead(2) == 'll':
            token = Token(R_ALL)
            advance = 3

        elif self.get_chr() == 'f' and self.lookahead(4) == 'irst':
            token = Token(R_FIRST)
            advance = 5

        elif self.get_chr() == 'l' and self.lookahead(3) == 'ast':
            token = Token(R_LAST)
            advance = 4

        elif self.get_chr() == 'o' and self.lookahead() == 'f':
            token = Token(R_OF)
            advance = 2
        
        elif self.get_chr() == 'i' and self.lookahead() == 'n':
            token = Token(IN)
            advance = 2

        elif self.get_chr() == 'w' and self.lookahead(4) == 'here':
            token = Token(R_WHERE)
            advance = 5

        elif self.get_chr().isalpha() or self.get_chr() == '_':
            token = self._consume_symbol()

        elif self.get_chr().isnumeric():
            token = self._consume_integer()

        elif self.get_chr() == '\n':
            token = Token(NEWLINE)
            advance = 1

        elif self.get_chr() == '(':
            token = Token(LPAR, '(')
            advance = 1

        elif self.get_chr() == ')':
            token = Token(RPAR, '')
            advance = 1

        elif self.get_chr() == '[':
            token = Token(LSQRBR, '[')
            advance = 1

        elif self.get_chr() == ']':
            token = Token(RSQRBR, ']')
            advance = 1

        elif self.get_chr() == '"':
            self._advance()
            token = self._consume_string('"')

        elif self.get_chr() == "'":
            self._advance()
            token = self._consume_string("'")

        elif self.get_chr() == ',':
            token = Token(COMMA, ',')
            advance = 1

        elif self.get_chr() == '=':
            token = Token(COMP_EQ, '=')
            advance = 1

        elif self.get_chr() == '<':
            if self.lookahead() == '=':
                token = Token(COMP_LT_EQ, '<=')
                advance = 2
            else:
                token = Token(COMP_LT, '<')
                advance = 1

        elif self.get_chr() == '>':
            if self.lookahead() == '=':
                token = Token(COMP_GT_EQ, '>=')
                advance = 2
            else:
                token = Token(COMP_GT, '>')
                advance = 2

        elif self.get_chr() == '!':
            if self.lookahead() == '=':
                token = Token(COMP_NOT_EQ, '!=')
                advance = 2
            else:
                advance = 1

        else:
            raise SyntaxError(
                "Unrecognized token '{0}'".format(self.get_chr()))

        for _ in range(0, advance):
            self._advance()

        if token is None:
            raise ParseError('Could not determine type of token')

        return token

    def _consume_symbol(self):
        name = ''

        while (self.get_chr() is not None) and (
                self.get_chr().isalpha() or self.get_chr().isnumeric() or self.get_chr() == '_'):
            name += self.get_chr()
            self._advance()

        return Token(SYMBOL, name)

    def _consume_string(self, delim):
        val = ''

        while self.get_chr() != delim:
            
            if self.get_chr() == '\n' or self.get_chr() is None:
                raise SyntaxError('Unterminated string')

            val += self.get_chr()
            self._advance()

        self._advance()
        return Token(STRING, val)

    def _consume_integer(self):
        val = ''

        while self.get_chr() is not None and self.get_chr().isnumeric():
            val += self.get_chr()
            self._advance()

        return Token(INTEGER, int(val))
