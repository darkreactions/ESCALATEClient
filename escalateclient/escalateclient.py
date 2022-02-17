from __future__ import annotations

from .core.base import BaseClient
from .core.experiment import ExperimentAPIMixin
from .core.organization import OrganizationAPIMixin

class ESCALATEClient(ExperimentAPIMixin,
                     OrganizationAPIMixin,
                     BaseClient):
    """ESCALATE API Client"""

    # def get_experiment_templates()
