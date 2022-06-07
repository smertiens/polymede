from query import QueryRunner
import sys

def end():
    print('Goodbye.')
    sys.exit(0)

def main():
    print('json-query')
    
    runner = QueryRunner()

    while True:
        try:
            query = input('> ')
        except KeyboardInterrupt:
            end()            

        if query.strip() == 'quit':
            end()
        else:
            # handle command
            result = runner.run_query(query)
            print(result)

if __name__ == '__main__':
    main()