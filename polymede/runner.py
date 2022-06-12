import json
from this import d
from tkinter import N
from polymede.tokenizer import Tokenizer
from polymede.parser import Parser, ParserError
from polymede.ast import *
from polymede.jsonpath import JSONPath
from polymede.exceptions import RuntimeError

class QueryRunner:
    """ Serves as the frontend to the query engine """

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
    """ Executes the AST returned from the parsing step """
    def __init__(self) -> None:
        self._data = None
    
    def _get_data(self):
        """Return the data that was loaded using the LOAD command.
            The data property should not be used directly so we can raise an exception 
            if no data has been loaded.
        """
        if self._data is None:
            raise RuntimeError('There is no data loaded. Load data with "load".')
        else:
            return self._data

    def run(self, ast: Query) -> dict:
        """ Run the Query tree """
        result = None

        if isinstance(ast.command, LoadCommand):
            result = self.load(ast.command.src, ast.command.format)
        
        elif isinstance(ast.command, FindCommand):
            result = self._find(ast.command)

        elif isinstance(ast.command, CountCommand):
            result = self._find(ast.command)
            result = len(result)

        return result

    def _apply_where(self, where: Where, data):
        """ Filter the given results through the WHERE expressions """        
        final_results = []
        for row in data:
            jp = JSONPath(where.lval, row)
            lval = jp.get_result()
            rval = where.rval
            op = where.op

            if lval is None:
                # If path does not exist in this row it will be skipped
                continue

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

    def _find(self, ast: AST):
        """ Find command """
        result = None

        jp = JSONPath(ast.selector, self._get_data())
        result = jp.get_result()

        if ast.where is not None:
            result = self._apply_where(ast.where, result)
        
        # since COUNT command is also processed here we have to check which node we are 
        # looking at right now
        if isinstance(ast, FindCommand): 
            if ast.fields is not None:
                field_selected_results = []
                if type(result) is not list:
                    result = [result]
                
                for row in result:
                    tmp = {}
                    for field in ast.fields:
                        try:
                            tmp[field] = row[field]
                        except KeyError:
                            raise ParserError('Unknown field "%s"' % field)
                    
                    field_selected_results.append(tmp)
                
                result = field_selected_results
            
            if ast.sortBy is not None:
                if isinstance(ast.sortBy, sort):
                    result = self._sort(ast.sortBy, result)

                elif isinstance(ast.sortBy, sortBy):
                    result = self._sortBy(ast.sortBy, result)

        return result

    def _sort(self, sort: sort, data):
        """ Processes a sort-Node by sorting a list in the given direction and returning it """
        return sorted(data, reverse = (True if sort.direction == "desc" else False))
            

    def _sortBy(self, sortBy: sortBy, data):
        """ Processes a sortBy-Node by sorting a nested list in the given direction and returning it """
        return sorted(data, key=lambda item: item[sortBy.field],
                reverse = (True if sortBy.direction == "desc" else False)
            )

    def load(self, src, format = 'auto'):
        """ Load data into memory """
        with open(src, 'r') as fp:
            self._data = json.load(fp)

        return True