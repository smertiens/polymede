import json
import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
os.chdir(os.path.dirname(__file__))

import query

def test_load_basic():
    runner = query.QueryRunner()
    runner.run_query('')


def test_load_command():
    runner = query.QueryRunner()
    
    assert runner.run_query('load "test.json"') == {'result': True}
    assert runner.run_query('load "test.json" as "json"') == {'result': True}


def test_find_all():
    runner = query.QueryRunner()
    
    assert runner.run_query('load "test2.json"') == {'result': True}

    assert runner.run_query('find "*" where "*.project" = 12')