import json
import pytest
from polymede.runner import QueryRunner
from polymede.parser import ParserError

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

def test_count(testdata_path):
    runner = QueryRunner()
    assert runner.run_query('load "%s/data_wuppertal.json"' % testdata_path) == True
    assert runner.run_query('count "fields"') == 18
    assert runner.run_query('count "features"') == 9985
    assert runner.run_query('count "features" where "attributes.Geschlecht" = "M"') == 4745
    assert runner.run_query('count "features" where "attributes.Geschlecht" = "W"') == 5039
    assert runner.run_query('count "features" where "attributes.Geschlecht" = "unbekannt"') == 201

def test_fail_on_unknown_command():
    runner = QueryRunner()
    
    with pytest.raises(ParserError) as ex:
        runner.run_query('dont know')
        assert 'Unknown command' in ex.__str__()