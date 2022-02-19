from __future__ import annotations

from .core.base import BaseClient
from .core.experiment import ExperimentAPIMixin
from .core.chemistry import ChemistryAPIMixin

class ESCALATEClient(ExperimentAPIMixin, 
                     ChemistryAPIMixin,
                     BaseClient):
    """ESCALATE API Client"""

    # def get_experiment_templates()
