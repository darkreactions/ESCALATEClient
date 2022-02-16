from __future__ import annotations
import json
import requests
from .exceptions import LoginError


class BaseClient:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url = base_url
        self._token = None
        self._selected_lab = None
        self.login(username, password)

    def login(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        r_login = requests.post(
            f"{self.base_url}/api/login",
            data={"username": self.username, "password": self.password},
        )

        if "token" in r_login.json():
            self._token = r_login.json()["token"]
            self._token_header = {"Authorization": f"Token {self._token}"}
            self._is_logged_in = True
        else:
            self._is_logged_in = False
            raise LoginError(r_login)

    def get(
        self,
        endpoint: str = "",
        data: dict = {},
        parse_json: bool = True,
        content_type: str = "application/json",
    ) -> dict | requests.Response | None:
        """Make GET request with `data` to `endpoint` in ESCALATE API

        return: (dict|list|requests.Response), bool
        """
        r = requests.get(
            f"{self.base_url}/api/{endpoint}",
            params=data,
            headers={**self._token_header, "content-type": content_type},
        )
        if r.ok:
            resp_json = r.json()
            if "count" in resp_json:
                print(f'GET: OK. Found {resp_json["count"]} results')
            else:
                print(f"GET: OK.")

            if parse_json:
                return resp_json.get("results", resp_json)
            else:
                return r
        else:
            print("GET: FAILED")
            print(f"Status {r.status_code}: {r.reason} {r.text}")

        return r

    def post(self, endpoint: str, data: dict, content_type: str = "application/json"):
        """POST `data` to `endpoint`in ESCALATE API using `content_type`
        return: (dict|requests.Response), bool
        """

        if not self._is_logged_in:
            raise ValueError("Not logged in: cannot post")

        r = requests.api.post(
            f"{self.base_url}/api/{endpoint}",
            data=json.dumps(data),
            headers={**self._token_header, "content-type": content_type},
        )
        # print(r)
        if r.ok:
            print("POST: OK, returning new resource dict")
            return r.json()
        print("POST: FAILED, returning response object")
        print(f"Status {r.status_code}: {r.reason} {r.text}")
        return r

    def _generate_url(
        self, url: str = None, endpoint: str = None, resource_id: str = None
    ):
        if not url:
            if not (endpoint and resource_id):
                raise ValueError("Must specify either url or endpoint and resource_id")
            else:
                url = f"{self.base_url}/api/{endpoint}/{resource_id}/"
        return url

    def put(
        self,
        url: str = None,
        endpoint: str = None,
        resource_id: str = None,
        data: dict = None,
    ):
        """Update a resource
        Either provide a url or an endpoint and resource id
        """
        url = self._generate_url(url, endpoint, resource_id)
        r = requests.api.put(url, json=data, headers=self._token_header)
        print(f"Status {r.status_code}: {r.reason}")
        if not r.ok:
            print(f"{r.text}")
        return r.json()

    def patch(
        self,
        url: str = None,
        endpoint: str = None,
        resource_id: str = None,
        data: dict = None,
    ):
        url = self._generate_url(url, endpoint, resource_id)
        r = requests.api.patch(url, json=data, headers=self._token_header)
        print(f"Status {r.status_code}: {r.reason}")
        if not r.ok:
            print(f"{r.text}")
        return r.json()

    def delete(self, url: str = None, endpoint: str = None, resource_id: str = None):
        """Delete a resource
        Either provide a url or an endpoint and resource id
        """
        url = self._generate_url(url, endpoint, resource_id)
        r = requests.api.delete(url, headers=self._token_header)
        print(f"Status {r.status_code}: {r.reason}")
        if not r.ok:
            print(f"{r.text}")
        return r.json()

    def list_endpoints(self):
        return self.get()
