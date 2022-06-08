from query import QueryRunner
import sys, os, json
import colorama

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalTrueColorFormatter

try:
    import readline
except ImportError:
    pass

historyPath = os.path.join(os.path.expanduser('~'), '.json_query.history')

def end():
    if readline:
        readline.set_history_length(1000)
        readline.write_history_file(historyPath)

    print('Goodbye.')
    sys.exit(0)

def main():
    colorama.init()

    if readline:
        try:
            readline.read_history_file(historyPath)

        except FileNotFoundError:
            pass

    print('json-query')
    
    runner = QueryRunner()

    while True:
        try:
            query = input('> ')
            
            if readline:
                readline.add_history(query)
        except KeyboardInterrupt:
            end()            

        if query.strip() == 'quit':
            end()
        else:
            # handle command
            try:
                result = runner.run_query(query)
                formatted = json.dumps(result, indent=2)
                highlighted = highlight(formatted, get_lexer_by_name('json'), TerminalTrueColorFormatter())
                print(highlighted)

            except Exception as ex:
                print(colorama.Fore.RED +
                    'Error while executing query (%s): %s' % (type(ex).__name__, ex.__str__()) +
                    colorama.Fore.RESET
                    )
                
                raise ex

if __name__ == '__main__':
    main()