import json
import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
os.chdir(os.path.dirname(__file__))

from query import JSONPath

def test_basic():

    cases = [
        ('foo', {"foo": "bar"}, 'bar'),
        ('foo.bar', {"foo": {"bar": {"baz": 23}}}, {"baz": 23}),
        ('foo.bar.baz', {"foo": {"bar": {"baz": 23}}}, 23)
    ]

    for case in cases:
        jp = JSONPath(case[0], case[1])
        assert jp.get_result() == case[2]



def test_asterisk():

    cases = [
        ('*.foo', [{"foo": "bar"}, {"bar": "baz"}, {"bam": 12}, {"foo": 123}], ['bar', 123]),
        ('items.*.foo', {"items" : [{"foo": "bar"}, {"bar": "baz"}, {"bam": 12}, {"foo": 123}]}, ['bar', 123]),
        ('items.foo.*.name', {"items" : {
                "foo": [{"name": "Peter"}, {"name": "Mary"}]
                }
            }, ['Peter', 'Mary'])
    ]

    for case in cases:
        jp = JSONPath(case[0], case[1])
        assert jp.get_result() == case[2]
