from __future__ import annotations
from typing import Any, Tuple, Dict, List
import requests
from .constants import Endpoints
from .protocols import BaseClientProtocol, RTName, RTResponse, RMTName, RMTResponseList


class ExperimentAPIMixin:
    def get_experiment_template(
        self: BaseClientProtocol,
        name: str,
        details: bool = False,
        content_type: str = "application/json",
    ) -> "list[Any] | requests.Response":
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
        self: BaseClientProtocol,
        search: Dict[str, str] = {},
    ) -> "list[Any] | requests.Response":
        """
        Re
        Args:
            uuid (str): UUID of the experiment instance
            search (dict): Dictionary of search parameters
        """
        return self.get(endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data=search)

    def get_action_parameters(
        self: BaseClientProtocol, uuid: str
    ) -> "list[Any] | requests.Response":
        """Gets the action parameters related to the experiment instance defined by uuid

        Args:
            uuid (str): UUID of experiment instance
        """
        return self.get(
            endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data={"uuid": uuid}
        )

    def get_outcomes(
        self: BaseClientProtocol, uuid: str
    ) -> "list[Any] | requests.Response":
        """Get outcomes related to experiment instance defined by uuid

        Args:
            uuid (str): UUID of experiment instance
        """
        return self.get(
            endpoint=Endpoints.EXPERIMENT_INSTANCE.value, data={"uuid": uuid}
        )

    def create_reagent_templates(
        self: BaseClientProtocol, data: dict[RTName, dict[str, list[str]]]
    ):
        """Creates reagent templates based on data dict passed.
           If the chemical type does not exist, it is automatically created

        Args:
            data (dict[str, Any]): Dictionary of reagent template name as keys
                                   and a list of chemical types as value
        """
        reagent_template_responses: "dict[RTName, RTResponse]" = {}
        reagent_material_template_responses: "dict[RMTName, RMTResponseList]" = {}
        for reagent_template_name, template_data in data.items():
            reagent_template_data = {"description": reagent_template_name}
            """
            if 'properties' in template_data:
                props = template_data['properties']
                property_list = []
                for prop in props:
                    prop_data = {'description': prop}
                    property_response = self.get_or_create(endpoint='property-template', data=prop_data)[0]
                    property_list.append(property_response['url'])
                reagent_template_data
            """

            reagent_response: RTResponse = self.get_or_create(
                endpoint="reagent-template", data=reagent_template_data
            )[0]

            rmt_responses: RMTResponseList = []

            if "chemical_types" in template_data:
                chem_types = template_data["chemical_types"]
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
                    rmt_response = self.get_or_create(
                        endpoint="reagent-material-template",
                        data=reagent_template_material_data,
                    )[0]
                    rmt_responses.append(rmt_response)

            reagent_template_responses[reagent_template_name] = reagent_response
            reagent_material_template_responses[reagent_template_name] = rmt_responses

        return reagent_template_responses, reagent_material_template_responses

    def create_action_parameters(
        self: BaseClientProtocol, data: dict[str, Tuple[str, str]]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Creates action definitions and their related parameter definitions using a simple
        dictionary.

        Args:
            data (dict[str, Any]): Defines action defs and parameter defs. Key is action def and value is a list of
            tuples of parameter defs and default values
        """

        action_def_response: Dict[str, Any] = {}
        action_parameter_response: Dict[str, Any] = {}

        for action_def, parameter_def_list in data.items():
            ap_data_list: List[Dict[str, Any]] = []
            for (parameter_def, default_value) in parameter_def_list:
                ap_data = {"description": parameter_def, "default_val": default_value}
                action_parameter_response[parameter_def] = self.get_or_create(
                    endpoint="parameter-def", data=ap_data
                )[0]
                ap_data_list.append(action_parameter_response[parameter_def]["url"])

            ad_data: Dict[str, Any] = {
                "description": action_def,
                "parameter_def": ap_data_list,
            }
            action_def_response[action_def] = self.get_or_create(
                endpoint="action-def", data=ad_data
            )[0]
            print(parameter_def_list)

        return action_def_response, action_parameter_response
