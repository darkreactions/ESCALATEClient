# ESCALATEClient

A convenient python interface to the ESCALATE REST API. 

## Installation 
1. `git clone` this repo
2. from the repository root directory, run `pip install .`

## Basic usage

```python
from escalateclient import ESCALATEClient

escalate=ESCALATEClient(escalate_url, 
                        username, 
                        password)

escalate.list_endpoints()

escalate.get(endpoint, data={})
escalate.post(endpoint, data={})
escalate.put(resource_url, data={})
escalate.delete(resource_url)
```
