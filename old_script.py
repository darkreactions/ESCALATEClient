# %%
import requests
from requests.api import patch
import importlib
#from escalateclient.escalateclient import ESCALATEClient
import escalateclient
importlib.reload(escalateclient)

escalate = escalateclient.escalateclient.ESCALATEClient(
    'http://localhost:8000', 'vshekar', 'copperhead123')

# %%
escalate.get_experiment_template('Workflow 1')

# %%
uuid = '24fd8829-6e08-4c2b-b402-9b3cb54e2869'
data = escalate.get(endpoint='parameter', data={
                    'uuid': uuid})
# %%
print(data)
data = data[0]
# %%
# escalate.post()
data['parameter_val_actual']['value'] = 600
# %%
a = escalate.put(endpoint='parameter', resource_id=data['uuid'], data=data)
# %%
r = requests.api.put(f'http://localhost:8000/api/parameter/{uuid}/',
                     json=data, headers=escalate._token_header)
# %%
patch_data = {'parameter_val_actual': data['parameter_val_actual']}
# %%
patch_data
# %%

escalate.patch(endpoint='parameter', resource_id=data['uuid'], data=data)

# %%
r = requests.api.get(f'http://localhost:8000/api/parameter/{uuid}/',
                     headers=escalate._token_header)
# %%
r = requests.api.patch(f'http://localhost:8000/api/parameter/{uuid}/',
                       json=patch_data, headers=escalate._token_header)
# %%
r


# %%
