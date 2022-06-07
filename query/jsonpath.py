import re

class PathError(Exception):
    pass

class JSONPath:

    re_items = re.compile(r'(?P<item>\w+|\(.*\)|\*)\.*', re.IGNORECASE | re.MULTILINE)
    
    def __init__(self, path: str, data: any) -> None:
        self._path = path
        self._data = data
    
    def get_result(self):
        items = self._split()
        return self._walk_data(items, self._data)

    def _walk_data(self, items: list, data):
        if len(items) == 0:
            return data

        item = items[0]
        result = None

        if item == '*':
            result = []

            for child in data:
                res = self._walk_data(items[1:], child)
                if res is not None:
                    result.append(res)

            return result

        else:
            if item in data:
                return self._walk_data(items[1:], data[item])
            
            else:
                return None

    def _split(self) -> list:
        
        matches = self.re_items.finditer(self._path)
        items = []
        
        for match in matches:
            items.append(match.group('item'))
        
        return items

