from __future__ import annotations
from .constants import Endpoints


class ChemistryAPIMixin:
    def get_inventory_material(self, search: dict = {}):
        """[summary]

        Args:
            search (dict, optional): [description]. Defaults to {}.
        """
        ...
        endpoint = f"{Endpoints.INVENTORY_MATERIAL.value}"
        if len(search)>0:
            query_parameters_list = [
            f"{q}={p}" if not p.startswith("!") else f"{q}!={p[1:]}"
            for q,p in search.items()
            ]

            query_parameters = '&'.join(query_parameters_list)
            endpoint = f"{endpoint}?{query_parameters}"
        
        materials = self.get(endpoint=endpoint)
        return materials


