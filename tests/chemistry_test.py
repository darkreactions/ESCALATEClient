import pytest
from escalateclient.conftest import client


def test_get_exact(client):
    search={
        "uuid": "24d9e08b-0a4f-4683-b7e1-293cc5117438"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if material["uuid"] != "24d9e08b-0a4f-4683-b7e1-293cc5117438":
            assert False
    assert True 


def test_get_fields(client):
    search={
        "fields": "phase,description"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if len(material) != 2 or "phase" not in material or "description" not in material:
            assert False
    assert True

def test_get_omit_field(client):
    search = {
        "omit": "phase,description"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if "phase" in material or "description" in material:
            assert False
    assert True 

def test_get_iexact(client):
    search={
        "description__iexact": "1,4-Benzene diammonium iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if material["description"] != "1,4-Benzene diammonium iodide":
            assert False
    assert True

def test_get_iexact_case(client):
    search={
        "description__iexact": "1,4-BenzeNE diaMMonium iODIde"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if material["description"] != "1,4-Benzene diammonium iodide":
            assert False
    assert True

def test_get_contains(client):
    search={
        "description__contains": "iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if "iodide" not in material["description"]:
            assert False
    assert True

def test_get_contains_case(client):
    search={
        "description__contains": "IOdidE"
        }
    res = client.get_inventory_material(search)
    if len(res) > 0:
        assert False
    assert True

def test_get_icontains(client):
    search={
        "description__contains": "iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if "iodide" not in material["description"]:
            assert False
    assert True

def test_get_icontains_case(client):
    search={
        "description__contains": "IOdidE"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if "iodide" not in material["description"]:
            assert False
    assert True
    