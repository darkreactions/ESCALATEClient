from __future__ import annotations
from .constants import Endpoints


class OrganizationAPIMixin:
    def get_lab(self, search: dict = {}):
        """Gets the lab/organization based on search terms, otherwise returns all labs

        Args:
            search (dict, optional): [description]. Defaults to {}.
        search = {
            query: parameter,
            query: !parameter
        }
        """
        endpoint = f"{Endpoints.ORGANIZATION.value}/"
        if len(search) > 0:
            # if param doesnt start with ! then it is normal equals
            # if it starts with ! then the query is negated and the leading ! is stripped
            query_parameters_list = [
                f"{q}={p}" if not p.startswith("!") else f"{q}!={p[1:]}"
                for q,p in search.items()
            ]
            query_parameters = "&".join(query_parameters_list)
            endpoint = f"{endpoint}?{query_parameters}"
        labs = self.get(endpoint=endpoint)
        return labs

    def select_lab(self, uuid: str):
        """Selects the lab based on the uuid. Variable to be set is self._selected_lab

        Args:
            uuid (str): uuid of the lab
        """
        endpoint = f"{Endpoints.ORGANIZATION.value}/{uuid}"
        lab = self.get(endpoint=endpoint)
        # return true or false whether selecting lab was successful
        if "uuid" in lab:
            self._selected_lab = lab
            return True 
        else:
            return False
