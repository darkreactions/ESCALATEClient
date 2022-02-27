from __future__ import annotations
from typing import Any, Tuple
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
        return self.get(endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data={'uuid': uuid})

    def get_outcomes(self, uuid: str):
        """Get outcomes related to experiment instance defined by uuid

        Args:
            uuid (str): UUID of experiment instance
        """
        return self.get(endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data={'uuid': uuid})

    def create_reagent_templates(self, data: dict[str, Any]):
        """Creates reagent templates based on data dict passed.
           If the chemical type does not exist, it is automatically created

        Args:
            data (dict[str, Any]): Dictionary of reagent template name as keys
                                   and a list of chemical types as value
        """
        reagent_template_responses = {}
        for reagent_template_name, chem_types in data.items():
            reagent_template_data = {"description": reagent_template_name}
            reagent_response = self.get_or_create(
                endpoint="reagent-template", data=reagent_template_data
            )[0]
            for chem_type in chem_types:
                chemical_type_data = {"description": chem_type}
                chemical_type_response = self.get_or_create(
                    endpoint="material-type", data=chemical_type_data
                )[0]
                reagent_template_material_data = {
                    "description": f"{reagent_template_name}: {chem_type}",
                    "reagent_template": reagent_response["url"],
                    "material_type": chemical_type_response["url"],
                }
                rtm_response = self.get_or_create(
                    endpoint="reagent-material-template",
                    data=reagent_template_material_data,
                )
            reagent_template_responses[reagent_template_name] = reagent_response

        return reagent_template_responses

    def create_action_parameters(self, data: dict[str, Tuple[str, str]]):
        """Creates action definitions and their related parameter definitions using a simple
        dictionary.

        Args:
            data (dict[str, Any]): Defines action defs and parameter defs. Key is action def and value is a list of
            tuples of parameter defs and default values
        """

        action_def_response = {}
        action_parameter_response = {}

        for action_def, parameter_def_list in data.items():
            ad_data = {"description": action_def}
            action_def_response[action_def] = self.get_or_create(
                endpoint="action-def", data=ad_data
            )[0]
            print(parameter_def_list)
            for (parameter_def, default_value) in parameter_def_list:
                ap_data = {"description": parameter_def, "default_value": default_value}
                action_parameter_response[parameter_def] = self.get_or_create(
                    endpoint="parameter-def", data=ap_data
                )[0]

        return action_def_response, action_parameter_response

        # This action definition stores the volume to be dispensed defined as a parameter definition
        data = {
            "description": "volume",
            "default_value": {"type": "num", "unit": "mL", "value": 0.0},
        }
        volume_parameter_def_response = self.get_or_create(
            endpoint="parameter-def", data=data
        )[0]
