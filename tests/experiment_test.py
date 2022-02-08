import pytest
from escalateclient.conftest import client


def test_get_exp_template_details(client):
    res = client.get_experiment_template('Workflow 1', details=True)
    assert 'Workflow 1' in res[0]['description']

def test_get_exp_template(client):
    res = client.get_experiment_template('Workflow 1')
    assert 'experiment_parameters_1' in res