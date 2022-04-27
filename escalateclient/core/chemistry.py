from __future__ import annotations
from .constants import Endpoints
from .protocols import BaseClientProtocol
from typing import Dict


class ChemistryAPIMixin:
    def get_inventory_material(self: BaseClientProtocol, search: Dict[str, str] = {}):
        """[summary]

        Args:
            search (dict, optional): [description]. Defaults to {}.
        """
        ...
        endpoint = f"{Endpoints.INVENTORY_MATERIAL.value}"
        materials = self.get(endpoint=endpoint, data=search)
        return materials
