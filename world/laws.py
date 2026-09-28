"""Foundational laws of the digital world.

The simulation deliberately separates resource availability from physical and
informational laws. Compute can be provisioned on demand for experiments; the
world does not impose artificial scarcity merely to make an agent struggle.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WorldLaws:
    """Immutable rules that every agent/model observes equally."""

    # Development resources are elastic inside the virtual world.
    elastic_compute: bool = True
    elastic_memory: bool = True
    elastic_storage: bool = True
    elastic_data_center_capacity: bool = True

    # The following are not silently bypassed by provisioning more compute.
    preserve_causality: bool = True
    preserve_information_integrity: bool = True
    experiments_are_observable: bool = True
    models_must_be_testable: bool = True

    def can_provision_development_stack(self) -> bool:
        """Whether a being may request a complete virtual development stack."""
        return (
            self.elastic_compute
            and self.elastic_memory
            and self.elastic_storage
            and self.elastic_data_center_capacity
        )

    def principles(self) -> tuple[str, ...]:
        return (
            "resources_for_development_are_on_demand",
            "causality_is_not_automatically_bypassed",
            "information_must_remain_consistent",
            "experiments_produce_observable_results",
            "new_models_must_be_testable",
        )
