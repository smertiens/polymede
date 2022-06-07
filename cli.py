from query import QueryRunner
import sys
import colorama

try:
    import readline
except ImportError:
    pass

def end():
    print('Goodbye.')
    sys.exit(0)

def main():
    colorama.init()

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
                print(result)

            except Exception as ex:
                print(colorama.Fore.RED +
                    'Error while executing query (%s): %s' % (type(ex).__name__, ex.__str__()) +
                    colorama.Fore.RESET
                    )

if __name__ == '__main__':
    main()