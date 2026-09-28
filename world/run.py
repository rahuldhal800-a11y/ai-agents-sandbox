"""Small executable demonstration of the digital world."""

from .actions import observe, remember
from .sim import create_world, spawn_entity, step


def run_demo(ticks: int = 20) -> dict:
    world = create_world()
    spawn_entity(world, "being-0001")

    for _ in range(ticks):
        observation = observe(world, "being-0001")
        remember(world, "being-0001", observation)
        step(world)

    return world.snapshot()


if __name__ == "__main__":
    print(run_demo())
