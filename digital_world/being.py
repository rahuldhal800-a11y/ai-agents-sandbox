"""Genesis: the first LLM-independent digital being prototype."""

from dataclasses import dataclass, field
from typing import Any

from .learner import Experience, Learner
from .memory import Memory
from .tools import ToolBox
from .world import World


@dataclass
class Genesis:
    name: str = "Genesis"
    world: World = field(default_factory=World)
    memory: Memory = field(default_factory=Memory)
    tools: ToolBox = field(default_factory=ToolBox)
    learner: Learner = field(default_factory=Learner)
    alive: bool = True

    def kill(self, reason: str = "Operator emergency stop") -> None:
        self.alive = False
        self.memory.remember(self.world.clock, "kill", {"reason": reason, "being": self.name})

    def reset(self) -> None:
        self.alive = True
        self.memory.remember(self.world.clock, "reset", {"being": self.name})

    def perceive(self) -> dict[str, Any]:
        observation = self.world.observe()
        self.memory.remember(self.world.clock, "observation", observation)
        return observation

    def discover_tools(self) -> list[str]:
        return self.tools.names()

    def act(self, action: str, **kwargs: Any) -> Any:
        if not self.alive:
            return {"status": "killed", "being": self.name}
        result = self.tools.call(action, **kwargs)
        self.memory.remember(self.world.clock, "action", {"action": action, "result": str(result)})
        return result

    def learn_from_result(self, goal: str, action: str, result: Any, reward: float) -> None:
        self.learner.learn(Experience(goal, action, result, reward))
        self.memory.remember(self.world.clock, "learning", {"goal": goal, "action": action, "reward": reward})

    def run_cycle(self, goal: str, action: str, **kwargs: Any) -> Any:
        if not self.alive:
            return {"status": "killed", "being": self.name}
        self.perceive()
        result = self.act(action, **kwargs)
        reward = 0.0 if isinstance(result, dict) and result.get("status") == "error" else 1.0
        self.learn_from_result(goal, action, result, reward)
        self.world.step()
        return result
