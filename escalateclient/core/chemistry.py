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
        materials = self.get(endpoint=endpoint, data=search)
        return materials


