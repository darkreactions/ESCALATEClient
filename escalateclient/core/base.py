from __future__ import annotations
import json
import requests
from urllib.parse import urlparse
from .exceptions import LoginError
from pathlib import Path
import uuid


class BaseClient:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url = base_url
        self.parsed_url = urlparse(self.base_url)
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

    def _remove_urls_and_dictionaries(self, data: dict):
        """Removes any urls or nested dictionaries in the dictionary because it is being passed as url
        params. If url belongs to escalate replace with the UUID otherwise remove it altogether

        Args:
            data (dict): Dictionary of search data
        """
        processed_data = {}
        for k, v in data.items():
            if not v:
                continue
            try:
                result = urlparse(v)
                if not result.netloc:
                    # print(f"Value of v: {v}")
                    processed_data[k] = v
                elif (
                    result.netloc == self.parsed_url.netloc
                ):  # Checks if its the same location as Escalate
                    uuid_string = Path(result.path).stem  # Gets uuid string
                    uuid.UUID(uuid_string)  # Verifies if its uuid
                    processed_data[
                        k
                    ] = uuid_string  # If url and uuid is verified, replace the key
                else:
                    continue

            except Exception as e:
                if not isinstance(v, dict):
                    processed_data[k] = v
        return processed_data

    def _construct_url(
        self, endpoint: str = "", resource_id: str = "", related_endpoint: str = ""
    ):
        url = f"{self.base_url}/api/{endpoint}"
        if resource_id:
            url = f"{url}/{resource_id}"
            if related_endpoint:
                url = f"{url}/{related_endpoint}"
        return url

    def get(
        self,
        endpoint: str = "",
        data: dict = {},
        resource_id: str = "",
        related_endpoint: str = "",
        parse_json: bool = True,
        content_type: str = "application/json",
    ) -> dict | requests.Response | None:
        """Make GET request with `data` to `endpoint` in ESCALATE API

        return: (dict|list|requests.Response), bool
        """
        data = self._remove_urls_and_dictionaries(data)
        print(data)
        url = self._construct_url(endpoint, resource_id, related_endpoint)
        r = requests.get(
            url,
            params=data,
            headers={**self._token_header, "content-type": content_type},
        )
        if r.ok:
            print(r.url)
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

    def post(
        self,
        endpoint: str,
        data: dict,
        resource_id: str = "",
        related_endpoint: str = "",
        content_type: str = "application/json",
    ):
        """POST `data` to `endpoint`in ESCALATE API using `content_type`
        return: (dict|requests.Response), bool
        """

        if not self._is_logged_in:
            raise ValueError("Not logged in: cannot post")
        url = self._construct_url(endpoint, resource_id, related_endpoint)
        r = requests.api.post(
            # f"{self.base_url}/api/{endpoint}/",
            # For post adding a trailing /
            url + "/",
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
        url = self._construct_url(endpoint=endpoint, resource_id=resource_id)
        r = requests.api.patch(url + "/", json=data, headers=self._token_header)
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

    def get_or_create(
        self,
        endpoint: str = None,
        resource_id: str = "",
        related_endpoint: str = "",
        data: dict = {},
    ):
        """Get resource matching data, else create a new one"""
        r = self.get(
            endpoint=endpoint,
            resource_id=resource_id,
            related_endpoint=related_endpoint,
            data=data,
        )
        if not len(r) > 0:
            r = [
                self.post(
                    endpoint=endpoint,
                    resource_id=resource_id,
                    related_endpoint=related_endpoint,
                    data=data,
                )
            ]
        return r

    def list_endpoints(self):
        return self.get()
