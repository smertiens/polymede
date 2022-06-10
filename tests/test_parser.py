import json
from polymede.runner import QueryRunner

def test_load_basic():
    runner = QueryRunner()
    runner.run_query('')


def test_load_command(testdata_path):
    runner = QueryRunner()
    
    assert runner.run_query('load "%s/test.json"' % testdata_path) == True
    assert runner.run_query('load "%s/test.json" as "json"' % testdata_path) == True


def test_find_all(testdata_path):
    runner = QueryRunner()
    
    assert runner.run_query('load "%s/test2.json"' % testdata_path) == True

    with open('%s/test2.json' % testdata_path) as fp:
        assert runner.run_query('find "*"') == json.load(fp)

def test_find_where(testdata_path):
    runner = QueryRunner()
    
    assert runner.run_query('load "%s/test.json"' % testdata_path) == True
    assert len(runner.run_query('find "projects.(1-10).meta"')) == 10
    
    res = runner.run_query('find "projects.(1-10).meta" where "name" != "statusmonitor"') 
    assert len(res) == 9

    res = runner.run_query('find "projects.(1-10).meta" where "name" = "statusmonitor"') 
    assert len(res) == 1

    with open('%s/test.json' % testdata_path) as fp:
        d = json.load(fp)
        assert res[0] == d['projects'][6]['meta']

def test_find_fields(testdata_path):
    runner = QueryRunner()
    assert runner.run_query('load "%s/test.json"' % testdata_path) == True
    res = runner.run_query('find (name, "warnings") in "projects.0.meta"')
    assert list(res[0].keys()) == ['name','warnings']

def test_find_where_fields(testdata_path):
    runner = QueryRunner()
    assert runner.run_query('load "%s/test.json"' % testdata_path) == True
    res = runner.run_query('find (size) in "projects.*.meta" where "name" = "alarmclock"')

    with open('%s/test.json' % testdata_path) as fp:
        d = json.load(fp)
        assert res[0] == { "size": d['projects'][0]['meta']['size'] }
