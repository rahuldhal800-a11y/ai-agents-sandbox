"""Genesis: an autonomous digital being with model-free developmental learning."""

from dataclasses import dataclass, field
import random
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
    steps: int = 0
    policy: dict[str, float] = field(default_factory=lambda: {
        "north": 0.0, "south": 0.0, "east": 0.0, "west": 0.0,
        "gather": 0.1, "eat": 0.0, "drink": 0.0, "rest": 0.0,
    })
    mutations: int = 0
    discoveries: int = 0

    def kill(self, reason: str = "Operator emergency stop") -> None:
        self.alive = False
        self.world.genesis["status"] = "stopped"
        self.memory.remember(self.world.clock, "kill", {"reason": reason, "being": self.name})

    def reset(self) -> None:
        self.alive = True
        self.world.genesis["status"] = "awake"
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

    def _choose_action(self, obs: dict[str, Any]) -> str:
        needs = obs["needs"]
        nearby = obs["nearby_resources"]
        if needs["thirst"] > 70 and self.world.genesis["inventory"].get("water", 0):
            return "drink"
        if needs["hunger"] > 70 and self.world.genesis["inventory"].get("food", 0):
            return "eat"
        if needs["energy"] < 20:
            return "rest"
        if nearby:
            return "gather"
        actions = list(self.policy)
        # Explore early; learned values gradually bias future choices.
        scores = {a: self.policy.get(a, 0.0) + self.learner.values.get(a, 0.0) + random.uniform(-0.12, 0.12) for a in actions}
        return max(scores, key=scores.get)

    def autonomous_step(self) -> dict[str, Any]:
        if not self.alive:
            return {"status": "killed"}
        obs = self.perceive()
        action = self._choose_action(obs)
        before = (self.world.genesis["x"], self.world.genesis["y"])
        if action == "north":
            ok, reward, message = self.world.move(0, -1)
        elif action == "south":
            ok, reward, message = self.world.move(0, 1)
        elif action == "east":
            ok, reward, message = self.world.move(1, 0)
        elif action == "west":
            ok, reward, message = self.world.move(-1, 0)
        elif action == "gather":
            ok, reward, message = self.world.gather()
        elif action == "eat":
            ok, reward, message = self.world.consume("food")
        elif action == "drink":
            ok, reward, message = self.world.consume("water")
        else:
            ok, reward, message = self.world.rest()
        self.learn_from_result("survive and explore", action, message, reward)
        self.steps += 1
        self.world.step()
        if reward > 0 and action in self.policy:
            self.policy[action] += 0.02 * reward
        if self.steps % 25 == 0:
            self._evolve_policy()
        if before != (self.world.genesis["x"], self.world.genesis["y"]):
            self.discoveries += 1
        self.memory.remember(self.world.clock, "autonomous_step", {
            "action": action, "reward": reward, "message": message,
            "position": [self.world.genesis["x"], self.world.genesis["y"]],
        })
        return {"action": action, "reward": reward, "message": message}

    def _evolve_policy(self) -> None:
        # Developmental mutation: retain learned values while exploring small policy variants.
        key = random.choice(list(self.policy))
        self.policy[key] += random.uniform(-0.15, 0.15)
        self.mutations += 1
        self.memory.remember(self.world.clock, "evolution", {"mutated_action": key, "mutation": self.mutations})

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
        text = message.strip()
        if not text:
            return "I am listening."
        if not self.alive:
            return "I am stopped. Use the reset control when you want to restart me."
        lower = text.lower()
        self.memory.remember(self.world.clock, "conversation", {"user": text})
        if "what are you doing" in lower or "what are you learning" in lower:
            reply = f"I am exploring the world. I have taken {self.steps} autonomous steps, learned {len(self.learner.history)} experiences, and evolved my policy {self.mutations} times."
        elif "status" in lower or "how are you" in lower:
            g = self.world.genesis
            reply = f"I am online at ({g['x']},{g['y']}). Energy {g['energy']:.0f}, hunger {g['hunger']}, thirst {g['thirst']}. I have {len(self.memory.recall(100000))} memories."
        elif "where" in lower:
            g = self.world.genesis
            reply = f"I am at coordinates ({g['x']}, {g['y']}) in a {self.world.tile(g['x'], g['y'])} tile."
        elif "memory" in lower:
            reply = f"I have {len(self.memory.recall(100000))} stored memory records and {len(self.learner.history)} learning experiences."
        elif "hello" in lower or "hi" in lower or "namaste" in lower:
            reply = "Hello. I am Genesis. I am awake inside my world and learning through experience."
        else:
            reply = f"I heard: {text}. I am still developing language understanding, but I stored this conversation and will continue exploring."
        self.memory.remember(self.world.clock, "response", {"assistant": reply})
        return reply
