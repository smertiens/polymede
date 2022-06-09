import json
import re
from .tokenizer import Tokenizer
from .parser import Parser, ParserError
from .ast import *
from .jsonpath import JSONPath

class RuntimeError(Exception):
    pass

class QueryRunner:

    def __init__(self, verbose = False) -> None:
        self.rt = Runtime()
        self._verbose = verbose
    
    def load(self, fname, format='auto') -> bool:
        return self.rt.load(fname)

    def run_query(self, query: str) -> dict:
        if query == '':
            return {}

        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(query)

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
        
        result = None

        if isinstance(ast.command, LoadCommand):
            result = self.load(ast.command.src, ast.command.format)
        
        elif isinstance(ast.command, FindCommand):
            result = self._find(ast.command.selector, ast.command.where, ast.command.fields)

        elif isinstance(ast.command, CountCommand):
            result = self._find(ast.command.selector, ast.command.where, None)
            result = len(result)

        return result

    def _apply_where(self, where: Where, data):
        
        final_results = []
        for row in data:
            jp = JSONPath(where.lval, row)
            lval = jp.get_result()
            rval = where.rval
            op = where.op

            if op == '=':
                if lval == rval:
                    final_results.append(row)
            elif op == '<':
                if lval < rval:
                    final_results.append(row)
            elif op == '>':
                if lval > rval:
                    final_results.append(row)
            elif op == '<=':
                if lval <= rval:
                    final_results.append(row)
            elif op == '>=':
                if lval >= rval:
                    final_results.append(row)
            elif op == '!=':
                if lval != rval:
                    final_results.append(row)
            else:
                raise RuntimeError("Unexpected operation.")

        return final_results

    def _find(self, selector, where, fields):
        
        result = None

        jp = JSONPath(selector, self._get_data())
        result = jp.get_result()

        if where is not None:
            result = self._apply_where(where, result)
        
        if fields is not None:
            field_selected_results = []
            if type(result) is not list:
                result = [result]
            
            for row in result:
                tmp = {}
                for field in fields:
                    try:
                        tmp[field] = row[field]
                    except KeyError:
                        raise ParserError('Unknown field "%s"' % field)
                
                field_selected_results.append(tmp)
            
            result = field_selected_results

        return result


    def load(self, src, format = 'auto'):

        with open(src, 'r') as fp:
            self._data = json.load(fp)

        return True