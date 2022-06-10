import pytest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

@pytest.fixture
def testdata_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__) + '/fixtures'))
