import json
import re
from .tokenizer import Tokenizer
from .parser import Parser
from .ast import *
from .jsonpath import JSONPath

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
            result = self._find(ast.command.selector)

        ret = {'result': result}

        return ret

    def _find(self, selector):
        filtered = None
        result = None

        jp = JSONPath(selector, self._data)
        return jp.get_result()

    def _load(self, src, format = 'auto'):

        with open(src, 'r') as fp:
            self._data = json.load(fp)

        return True