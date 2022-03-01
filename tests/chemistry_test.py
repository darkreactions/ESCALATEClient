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

def test_get_in(client):
    search={
        "description__in":"2-Pyrrolidin-1-ium-1-ylethylammonium iodide,"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if "2-Pyrrolidin-1-ium-1-ylethylammonium iodide" not in material["description"]:
            assert False 
    assert True 

def test_greater_than(client):
    search={
        "onhand_amt__gt":"2.0"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if material["onhand_amt"]["value"] <= 2.0:
            assert False 
    assert True 

def test_greater_than_equals(client):
    search={
        "onhand_amt__gte":"2.0"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if material["onhand_amt"]["value"] < 2.0:
            assert False 
    assert True 

def test_less_than(client):
    search={
        "onhand_amt__lt":"2.0"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if material["onhand_amt"]["value"] >= 2.0:
            assert False 
    assert True 

def test_less_than_equal(client):
    search={
        "onhand_amt__lte":"2.0"
    }
    res = client.get_inventory_material(search)
    for material in res:
        if material["onhand_amt"]["value"] >= 2.0:
            assert False 
    assert True 

def test_get_startwith(client):
    search={
        "description__startswith": "4-Fluoro"
        }
    res = client.get_inventory_material(search)
    if len(res) < 1: 
        assert False
    for material in res:
        if "4-Fluoro" not in material["description"]:
            assert False
    assert True

def test_get_istartwith(client):
    search={
        "description__istartswith": "4-FLUORO"
        }
    res = client.get_inventory_material(search)
    if len(res) < 1: 
        assert False
    for material in res:
        if "4-Fluoro" not in material["description"]:
            assert False
    assert True

def test_get_endwith(client):
    search={
        "description__endswith": "iodide"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if not material["description"].endswith("iodide"):
            assert False
    assert True

def test_get_iendwith(client):
    search={
        "description__iendswith": "ioDIDe"
        }
    res = client.get_inventory_material(search)
    for material in res:
        if not material["description"].endswith("iodide"):
            assert False
    assert True
