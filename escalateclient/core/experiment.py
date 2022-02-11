from __future__ import annotations
import json
import requests
from .constants import Endpoints


class ExperimentAPIMixin:
    def get_experiment_template(
        self, name: str, details: bool = False, content_type: str = "application/json"
    ) -> dict | None:
        """Retrieves the template of an experiment

        Args:
            name (str): Template name
            details (bool): Provides details of the template. Creation data if False
            content_type (str): Content type for request
        """

        exp_template_details = self.get(
            endpoint=Endpoints.EXPERIMENT_TEMPLATE.value, data={"description": name}
        )

        if not details:
            return self.get(
                f'{Endpoints.EXPERIMENT_TEMPLATE.value}/{exp_template_details[0]["uuid"]}/create'
            )
        else:
            return exp_template_details

    def get_experiment_instance(
        self,
        search: dict = {},
    ) -> dict | None:
        """
        Re
        Args:
            uuid (str): UUID of the experiment instance
            search (dict): Dictionary of search parameters
        """
        return self.get(endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data=search)

    def get_action_parameters(self, uuid: str):
        """Gets the action parameters related to the experiment instance defined by uuid

        Args:
            uuid (str): UUID of experiment instance
        """
        ...

    def get_outcomes(self, uuid: str):
        """Get outcomes related to experiment instance defined by uuid

        Args:
            uuid (str): UUID of experiment instance
        """
