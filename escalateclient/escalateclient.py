from __future__ import annotations

from .core.base import BaseClient
from .core.experiment import ExperimentAPIMixin

class ESCALATEClient(ExperimentAPIMixin,
                     BaseClient):
    """ESCALATE API Client"""

    # def get_experiment_templates()
