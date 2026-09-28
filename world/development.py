"""On-demand virtual development infrastructure."""

from dataclasses import dataclass

from .laws import WorldLaws


@dataclass(frozen=True)
class DevelopmentStack:
    """A virtual machine/data-center allocation for an experiment."""

    name: str
    cpu_cores: int
    memory_gb: int
    storage_tb: int
    accelerator_units: int
    data_center_nodes: int


class DevelopmentInfrastructure:
    """Provision development capacity without artificial scarcity."""

    def __init__(self, laws: WorldLaws | None = None) -> None:
        self.laws = laws or WorldLaws()
        self.stacks: dict[str, DevelopmentStack] = {}

    def provision_for_model(
        self,
        name: str,
        *,
        cpu_cores: int,
        memory_gb: int,
        storage_tb: int,
        accelerator_units: int = 0,
        data_center_nodes: int = 1,
    ) -> DevelopmentStack:
        """Instantly create the requested virtual development environment."""
        if not self.laws.can_provision_development_stack():
            raise RuntimeError("development infrastructure is disabled by world laws")
        values = (cpu_cores, memory_gb, storage_tb, accelerator_units, data_center_nodes)
        if any(value < 0 for value in values):
            raise ValueError("resource quantities cannot be negative")
        if data_center_nodes == 0:
            raise ValueError("at least one virtual data-center node is required")

        stack = DevelopmentStack(
            name=name,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            storage_tb=storage_tb,
            accelerator_units=accelerator_units,
            data_center_nodes=data_center_nodes,
        )
        self.stacks[name] = stack
        return stack

    def destroy(self, name: str) -> None:
        self.stacks.pop(name, None)
