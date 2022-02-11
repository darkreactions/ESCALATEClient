from __future__ import annotations
from .constants import Endpoints


class OrganizationAPIMixin:
    def get_lab(self, search: dict = {}):
        """Gets the lab/organization based on search terms, otherwise returns all labs

        Args:
            search (dict, optional): [description]. Defaults to {}.
        """
        ...

    def select_lab(self, uuid: str):
        """Selects the lab based on the uuid. Variable to be set is self._selected_lab

        Args:
            uuid (str): uuid of the lab
        """
        ...
