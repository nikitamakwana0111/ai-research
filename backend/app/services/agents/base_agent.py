from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    name: str

    @abstractmethod
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class AgentResult:
    def __init__(self, agent_name: str, output: str, metadata: Dict[str, Any] | None = None):
        self.agent_name = agent_name
        self.output = output
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "output": self.output,
            "metadata": self.metadata,
        }
