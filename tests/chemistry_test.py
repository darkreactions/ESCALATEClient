import pytest
from escalateclient.conftest import client


def test_get_inventory(client):
    search={
        "description": "1,4-Benzene diammonium iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if material["description"] != "1,4-Benzene diammonium iodide":
            assert False
    assert True

def test_get_exact(client):
    search={
        "description__iexact": "1,4-Benzene diammonium iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if material["description"] != "1,4-Benzene diammonium iodide":
            assert False
    assert True

def test_get_fields(client):
    search={
        "description__iexact": "1,4-Benzene diammonium iodide"
        }
    res = client.get_inventory_material(search)
    