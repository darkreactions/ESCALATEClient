import pytest
from escalateclient.conftest import client

def test_get_lab_no_search(client):
	search = {}
	labs = client.get_lab(search=search)
	assert isinstance(labs, list)

def test_get_lab_search_exact(client):
	search = {
		"full_name": "Haverford College"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if lab["full_name"] != "Haverford College":
			assert False
	assert True

def test_get_lab_search_iexact(client):
	search = {
		"full_name__iexact": "haverFORD ColLEGE"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if lab["full_name"] != "Haverford College":
			assert False
	assert True

def test_get_lab_search_fields(client):
	search = {
		"fields": "full_name,short_name"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if len(lab) != 2 or "full_name" not in lab or "short_name" not in lab:
			assert False
	assert True

def test_get_lab_search_omit(client):
	search = {
		"omit": "!full_name,short_name"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if "full_name" not in lab or "short_name" not in lab:
			assert False
	assert True

def test_get_lab_search_contains(client):
	search = {
		"full_name__contains": "College"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if "College" not in lab["full_name"]:
			assert False
	assert True

def test_get_lab_search_icontains(client):
	search = {
		"full_name__icontains": "collEGE"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if "college" not in lab["full_name"].lower():
			assert False
	assert True

def test_get_lab_search_in(client):
	names = ["Haverford College", "Lawrence Berkeley National Laboratory"]
	search = {
		"full_name__in": ",".join(names)
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if lab["full_name"] not in names:
			assert False
	assert True

def test_get_lab_search_startswith(client):
	search = {
		"full_name__startswith": "Haver"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if not lab["full_name"].startswith("Haver"):
			assert False
	assert True

def test_get_lab_search_istartswith(client):
	search = {
		"full_name__istartswith": "haVeR"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if not lab["full_name"].lower().startswith("haver"):
			assert False
	assert True

def test_get_lab_search_endswith(client):
	search = {
		"full_name__endswith": "College"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if not lab["full_name"].endswith("College"):
			assert False
	assert True

def test_get_lab_search_iendswith(client):
	search = {
		"full_name__iendswith": "colLEGE"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if not lab["full_name"].lower().endswith("college"):
			assert False
	assert True

def test_get_lab_search_negate(client):
	search = {
		"full_name": "!Haverford College"
	}
	labs = client.get_lab(search=search)
	for lab in labs:
		if lab["full_name"] == "Haverford College":
			assert False
	assert True

def test_select_lab(client):
	search = {
		"short_name": "LBL"
	}
	lbl = client.get_lab(search=search)
	uuid = lbl[0]["uuid"]
	assert client.select_lab(uuid=uuid)

def test_select_lab_bad_lab(client):
	uuid = "some-uuid-that-is-wrong"
	assert not client.select_lab(uuid=uuid)