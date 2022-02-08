import pytest
from .escalateclient import ESCALATEClient

@pytest.fixture
def client():
    return ESCALATEClient('http://localhost:8000', 'vshekar', 'copperhead123')
