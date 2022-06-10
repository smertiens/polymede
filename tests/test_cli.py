from polymede import cli
from click.testing import CliRunner
import json

def test_query(testdata_path):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['load "%s/test2.json"' % testdata_path])
    assert result.exit_code == 0
    assert result.output == 'true\n'

def test_load(testdata_path):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--load', '%s/test2.json' % testdata_path, 'find "*"'])
    assert result.exit_code == 0
    assert '"bar": "baz"' in result.output

def test_format():
    # formats are not implemented yet
    pass

def test_silent(testdata_path):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--silent', '--load', '%s/test2.json' % testdata_path, 'find "*"'])
    assert result.exit_code == 0
    assert result.output == ''

def test_verbose():
    # no verbose output yet
    pass

def test_ugly(testdata_path):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--ugly', '--load', '%s/test2.json' % testdata_path, 'find "*"'])
    assert result.exit_code == 0
    assert result.output == '[{"foo": "bar"}, {"bar": "baz"}, {"bam": 12}]\n'
