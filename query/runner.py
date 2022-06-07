import json
import re
from .tokenizer import Tokenizer
from .parser import Parser
from .ast import *

class RuntimeError(Exception):
    pass

class QueryRunner:

    def __init__(self) -> None:
        self.rt = Runtime()

    def run_query(self, query: str) -> dict:
        if query == '':
            return {}

        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(query)

        print(tokens)

        parser = Parser(tokens)
        ast = parser.parse()

        return self.rt.run(ast)


class Runtime:

    def __init__(self) -> None:
        self._data = None
    
    def _get_data(self):
        if self._data is None:
            raise RuntimeError('There is no data loaded. Load data with "load".')
        else:
            return self._data

    def run(self, ast: Query) -> dict:
        
        ret = {}
        result = None

        if isinstance(ast.command, LoadCommand):
            result = self._load(ast.command.src, ast.command.format)
        
        elif isinstance(ast.command, FindCommand):
            result = self._find(ast.command.range, ast.command.level, ast.command.selector)
        ret = {'result': result}

        return ret

    def _find(self, range, level, selector):
        filtered = None
        result = None

        if selector is None:
            filtered = self._get_data()

        print(filtered)

        if level == 'nested':
            pass
            
        if len(filtered) == 0:
            result = {}

        if range == 'first':
            result = filtered[0]
        elif range == 'last':
            result = filtered[len(filtered) - 1]
        elif range == 'all':
            result = filtered
        
        return result

    def _load(self, src, format = 'auto'):

        with open(src, 'r') as fp:
            self._data = json.load(fp)

        return True