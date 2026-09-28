"""Bootstrap Genesis without an AI API or pretrained model."""

from .being import Genesis
from .tools import Tool
from .world import World


def create_genesis() -> Genesis:
    being = Genesis(world=World())
    being.tools.register(Tool(
        name="observe_world",
        description="Observe the current digital world state.",
        function=lambda: being.world.observe(),
    ))
    being.tools.register(Tool(
        name="write_world",
        description="Write a value into the digital world state.",
        function=lambda key, value: being.world.write(key, value),
    ))
    return being


if __name__ == "__main__":
    genesis = create_genesis()
    print(genesis.run_cycle("learn the world", "observe_world"))
