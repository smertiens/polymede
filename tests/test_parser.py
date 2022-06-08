import imp
import json
import os, sys
from fixtures import *
import query


def test_load_basic():
    runner = query.QueryRunner()
    runner.run_query('')


def test_load_command(testdata_path):
    runner = query.QueryRunner()
    
    assert runner.run_query('load "%s/test.json"' % testdata_path) == True
    assert runner.run_query('load "%s/test.json" as "json"' % testdata_path) == True


def test_find_all(testdata_path):
    runner = query.QueryRunner()
    
    assert runner.run_query('load "%s/test2.json"' % testdata_path) == True

    with open('%s/test2.json' % testdata_path) as fp:
        assert runner.run_query('find "*"') == json.load(fp)