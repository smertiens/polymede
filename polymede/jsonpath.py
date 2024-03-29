import re
from polymede.exceptions import PathError

class JSONPath:
    """Traverses JSON data with using a path string"""

    re_items = re.compile(r'(?P<item>\w+|\(.*\)|\*)\.*', re.IGNORECASE | re.MULTILINE)
    re_par = re.compile(r'^\(([^\(\)]*)\)$')
    re_digit = re.compile(r'^\d+$')
    re_range = re.compile(r'^(\w+)\-(\w+)$')
    re_indexlist = re.compile(r'^[\d,\s]+$')

    def __init__(self, path: str, data: any) -> None:
        """ Create a new instance

        path -- Path string
        data -- JSON data (as Python object)
        """
        self._path = path
        self._data = data
    
    def get_result(self):
        """ Return the data the pathstring points at or None """
        items = self._split()
        return self._walk_data(items, self._data)

    def _walk_data(self, items: list, data):
        """Walk the JSON data recursively until the complete pathstring is processed

        items -- List of pathstring items (returned from self._split())
        data -- JSON data of the current level
        """

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
            par_match = self.re_par.match(item)
            
            if par_match:
                # unpack expression
                item = par_match.group(1)
                
                # Range match (x-y)
                range_match = self.re_range.match(item)
                if range_match:
                    start = range_match.group(1)
                    end = range_match.group(2)
                    rng = [start, end]

                    # TODO: move symbol resolve to function
                    for idx, itm in enumerate(rng):
                        
                        if itm.isnumeric():
                            rng[idx] = int(itm)
                        else:
                            if itm == 'first':
                                rng[idx]  = 0
                            elif itm == 'last':
                                rng[idx]  = len(data) - 1
                            else:
                                raise PathError('Invalid selector: "%s"' % item)

                    # extract range
                    result = []
                    for n in range(rng[0], rng[1] + 1):
                        res = self._walk_data(items[1:], data[n])

                        if res is not None:
                            result.append(res)

                
                else:
                    # overwrite with the same item without parentheses
                    items[0] = item 
                    # try again to match as literal key (without parentheses)
                    result = self._walk_data(items, data)
                    
                return result
            
            else:
                # treat as literal key

                # list indices cannot be strings
                if type(data) == list and item.isnumeric():
                    item = int(item)
                    return self._walk_data(items[1:], data[item])

                elif item in data:
                    return self._walk_data(items[1:], data[item])
                
                else:
                    return None

    def _split(self) -> list:
        """ Splits the pathstring into seperate components using '.' as the delimiter. """
        matches = self.re_items.finditer(self._path)
        items = []
        
        for match in matches:
            items.append(match.group('item'))
        
        return items
