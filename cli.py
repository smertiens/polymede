from query import QueryRunner
import sys, os, json
import colorama
import click

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalTrueColorFormatter

DEBUG = True

try:
    import readline
except ImportError:
    pass

historyPath = os.path.join(os.path.expanduser('~'), '.json_query.history')

# TODO: add tests for cli
@click.command
@click.argument('query', required=False)
@click.option('--load', default="", type=str, help="Load the given file name")
@click.option('--format', default="auto", type=str, help="Set the file type when using load (defaults to 'auto')")
@click.option('--silent', default=False, is_flag=True, help="Suppress output")
@click.option('--verbose', default=False, is_flag=True, help="Increase verbosity")
@click.option('--ugly', default=False, is_flag=True, help="Turn off pretty-printing of JSON data")
@click.option('--no-highlighting', default=False, is_flag=True, help="Turns off syntax highlighting for JSON data")
def main(query, load, format, silent, verbose, ugly, no_highlighting):
    """ Explore and query JSON files from the console. 
        If QUERY is given, the program starts in non-interactive mode and runs it.
    """

    def handle_exception(ex):
        output(colorama.Fore.RED +
            'Error while executing query (%s): %s' % (type(ex).__name__, ex.__str__()) +
            colorama.Fore.RESET
            )

        if DEBUG:
            raise ex

    def end():
        if readline:
            readline.set_history_length(1000)
            readline.write_history_file(historyPath)

        output('Goodbye.')
        sys.exit(0)

    def output(text: str) -> None:
        if not silent:
            print(text)

    def output_result(json_result: str) -> None:
        if silent:
            return
        
        formatted = ""

        if not ugly:
            formatted = json.dumps(json_result, indent=2)
        else:
            formatted = json.dumps(json_result)

        if sys.stdout.isatty() and not no_highlighting:
            # TODO: check if the terminal supports color
            highlighted = highlight(formatted, get_lexer_by_name('json'), TerminalTrueColorFormatter())
            output(highlighted)
        else:
            output(formatted)

    colorama.init()

    if readline:
        try:
            readline.read_history_file(historyPath)
        except FileNotFoundError:
            pass

    runner = QueryRunner(verbose=verbose)
    
    # Load file from command line
    if load:
        try:
            runner.load(load, format)
        except Exception as ex:
            handle_exception(ex)

    # Execute query from command line and return (non-interactive mode)
    if query:
        try:
            result = runner.run_query(query)
            output_result(result)
            sys.exit(0)
        except Exception as ex:
            handle_exception(ex)
            sys.exit(1)

    # Start interactive mode
    output('json-query')

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
                output_result(result)

            except Exception as ex:
                handle_exception(ex)

if __name__ == '__main__':
    main()