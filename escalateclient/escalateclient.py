import json

import requests

class ESCALATEClient():
    """ESCALATE API Client"""
    
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self._token = None
        self._is_logged_in = False
        self._login()
        
    def _login(self):
        r_login = requests.post(f'{self.base_url}/api/login', 
                                data={'username': self.username, 
                                      'password': self.password})
        self._token = r_login.json()['token']
        self._token_header = {'Authorization': f'Token {self._token}'}
        self._is_logged_in = True
        
    def get(self, 
            endpoint='', 
            data=None, 
            parse_json=True, 
            content_type='application/json'):
        """Make GET request with `data` to `endpoint` in ESCALATE API
    
        return: (dict|list|requests.Response), bool
        """
        data = {} if data is None else data
        r = requests.get(f'{self.base_url}/api/{endpoint}',
                         params=data, 
                         headers={**self._token_header, 
                                  'content-type': content_type})
        if r.ok: 
            print('GET: OK')
        else: 
            print('GET: FAILED')
        
        if r.ok and parse_json:
            resp_json = r.json()        
            # handle cases: no vs one vs many results
            count = resp_json.get('count')
            if count is None or count == 0:
                return r.json()
            elif count == 1: 
                print('Found one resource, returning dict')
                return resp_json['results'][0]
            elif count >= 1: 
                print(f"Found {resp_json['count']} resources, returning list of dicts)")
                return r.json()['results']
        print('Returning response object')   
        return r
    
    def search(self, 
        endpoint='',
        related_ep=None, #for cross-searches
        search_field='',
        criteria= '',
        data=None, #must be a list
        exact=False,
        negate=False,
        parse_json=True, 
        content_type='application/json'):
    
        if negate==False:

            if exact==True:
                if data == None:
                    '''Returns all fields for exact match'''
                    if related_ep == None:

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}={criteria}', 
                                     headers={**self._token_header, 
                                              'content-type': content_type})
                    else: #cross-search 
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}={criteria}', 
                                     headers={**self._token_header, 
                                              'content-type': content_type})

                else:
                    '''Returns requested field(s) for exact match'''
                    i=0
                    data_string=''
                    while i<len(data)-1:
                        data_string+=data[i]+','
                        i+=1
                    data_string+=data[i]

                    if related_ep ==None:

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}={criteria}&fields={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}={criteria}&fields={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 

            else:


                if data == None:
                    '''Containment test; returns all fields'''

                    if related_ep == None:
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}__icontains={criteria}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}__icontains={criteria}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type})

                else:
                    '''Containment test; returns requested field(s)'''
                    i=0
                    data_string=''
                    while i<len(data)-1:
                        data_string+=data[i]+','
                        i+=1
                    data_string+=data[i]

                    if related_ep==None:
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}__icontains={criteria}&fields={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}__icontains={criteria}&fields={data_string}', 
                                             headers={**self._token_header, 
                                                      'content-type': content_type})
        else:
        #negations

            if exact==True:
                if data == None:
                    '''Returns all fields for exact match'''
                    if related_ep == None:

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}!={criteria}', 
                                     headers={**self._token_header, 
                                              'content-type': content_type})
                    else: #cross-search 
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}!={criteria}', 
                                     headers={**self._token_header, 
                                              'content-type': content_type})

                else:
                    '''Returns requested field(s) for exact match'''
                    i=0
                    data_string=''
                    while i<len(data)-1:
                        data_string+=data[i]+','
                        i+=1
                    data_string+=data[i]

                    if related_ep ==None:

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}={criteria}&fields!={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search

                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}!={criteria}&fields={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 

            else:


                if data == None:
                    '''Containment test; returns all fields'''

                    if related_ep == None:
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}__icontains!={criteria}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}__icontains!={criteria}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type})

                else:
                    '''Containment test; returns requested field(s)'''
                    i=0
                    data_string=''
                    while i<len(data)-1:
                        data_string+=data[i]+','
                        i+=1
                    data_string+=data[i]

                    if related_ep==None:
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{search_field}__icontains!={criteria}&fields={data_string}', 
                                         headers={**self._token_header, 
                                                  'content-type': content_type}) 
                    else: #cross-search
                        r = requests.get(f'{self.base_url}/api/{endpoint}/?{related_ep}__{search_field}__icontains!={criteria}', 
                                             headers={**self._token_header, 
                                                      'content-type': content_type})                       

        if r.ok: 
            print('GET: OK')
        else: 
            print('GET: FAILED')

        if r.ok and parse_json:
            resp_json = r.json()        
            # handle cases: no vs one vs many results
            count = resp_json.get('count')
            if count is None or count == 0:
                return r.json()
            elif count == 1: 
                print('Found one resource, returning dict')
                return resp_json['results'][0]
            elif count >= 1: 
                print(f"Found {resp_json['count']} resources, returning list of dicts)")
                return r.json()['results']
        print('Returning response object')   
        return r
        
    def post(self, 
             endpoint, 
             data, 
             content_type='application/json'):
        """POST `data` to `endpoint`in ESCALATE API using `content_type`
        return: (dict|requests.Response), bool
        """
        
        if not self._is_logged_in:
            raise ValueError("Not logged in: cannot post")
        
        r = requests.api.post(
            f'{self.base_url}/api/{endpoint}', 
            data=json.dumps(data), 
            headers={**self._token_header,
                     'content-type': content_type})
        print(r)
        if r.ok: 
            print('POST: OK, returning new resource dict')
            return r.json()
        print('POST: FAILED, returning response object')
        return r
    
    def put(self, url=None, endpoint=None, resource_id=None, data=None):
        """Update a complete resource
        Either provide a url or an endpoint and resource id
        """
        if not ((url is not None) or (endpoint is not None and resource_id is not None)): 
            raise ValueError("Must specify either url or endpoint and resource_id")
            
        if url is None: 
            url = f'{self.base_url}/api/{endpoint}/{resource_id}' 
        r = requests.api.put(url, data, headers=self._token_header)
        return r
    
    def patch(self, url=None, endpoint=None, resource_id=None, data=None):
        """Update parts of a resource
        Either provide a url or an endpoint and resource id
        """
        if not ((url is not None) or (endpoint is not None and resource_id is not None)): 
            raise ValueError("Must specify either url or endpoint and resource_id")
            
        if url is None: 
            url = f'{self.base_url}/api/{endpoint}/{resource_id}' 
        r = requests.api.patch(url, data, headers=self._token_header)
        return r
        
    def delete(self, url=None, endpoint=None, resource_id=None):
        """Delete a resource
         Either provide a url or an endpoint and resource id
        """
        if not ((url is not None) or (endpoint is not None and resource_id is not None)): 
            raise ValueError("Must specify either url or endpoint and resource_id")
        if url is None: 
            url = f'{self.base_url}/api/{endpoint}/{resource_id}' 
        r = requests.api.delete(url, headers=self._token_header)
        return r
    
    def list_endpoints(self):
        return self.get()
