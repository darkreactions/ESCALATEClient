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
        """

        exp_template_details = self.get(
            endpoint=Endpoints.EXPERIMENT_TEMPLATE.value, data={
                "description": name}
        )

        if not details:
            return self.get(
                f'{Endpoints.EXPERIMENT_TEMPLATE.value}/{exp_template_details[0]["uuid"]}/create'
            )
        else:
            return exp_template_details
