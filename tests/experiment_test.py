import pytest
from typing import Any, Iterable
from escalateclient.conftest import client
from escalateclient.escalateclient import ESCALATEClient


def test_get_exp_template_details(client: ESCALATEClient):
    res = client.get_experiment_template("Workflow 1", details=True)
    assert isinstance(res, list)
    assert "Workflow 1" in res[0]["description"]


def test_create_action_params(client: ESCALATEClient):
    data = {
        "test_action_template": [
            ("test_parameters", {"type": "num", "unit": "degC", "value": 0.0})
        ]
    }
    action_defs, paramter_defs = client.create_action_parameters(data=data)
    assert isinstance(action_defs, dict)
    assert isinstance(paramter_defs, dict)
    for pdef_data in paramter_defs.values():
        assert pdef_data["url"] in action_defs["test_action_template"]["parameter_def"]
