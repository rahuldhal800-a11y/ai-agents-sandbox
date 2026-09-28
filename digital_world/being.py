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

    def talk(self, message: str) -> str:
        """Small deterministic conversation layer; the cognitive engine will replace this."""
        text = message.strip()
        if not text:
            return "I am listening."
        if not self.alive:
            return "I am stopped. Use the reset control when you want to restart me."
        lower = text.lower()
        self.memory.remember(self.world.clock, "conversation", {"user": text})
        if any(word in lower for word in ("hello", "hi", "namaste", "hey")):
            reply = "Hello. I am Genesis. I am online and ready to explore this digital world."
        elif "status" in lower or "how are you" in lower:
            reply = f"I am online. World tick {self.world.clock}. I have {len(self.tools.names())} tools and {len(self.memory.records)} memory records."
        elif "tool" in lower:
            reply = "My current tools are: " + ", ".join(self.tools.names()) + "."
        elif "memory" in lower or "remember" in lower:
            reply = f"I currently have {len(self.memory.records)} memory records."
        elif "observe" in lower or "world" in lower:
            observation = self.perceive()
            reply = f"I observe the world at tick {self.world.clock}: {observation}."
        else:
            reply = f"I heard you say: {text}. My deeper reasoning system is still being built, but I recorded this interaction in memory."
        self.memory.remember(self.world.clock, "response", {"assistant": reply})
        self.world.step()
        return reply
"