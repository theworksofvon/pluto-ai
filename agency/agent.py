from pydantic import BaseModel
from typing import Callable, Union, Optional, List
from abc import ABC, abstractmethod
from .agency_types import Tendencies, Responsibilities, Roles
from config import config
from .communications import CommunicationProtocol
from .exceptions import CommunicationsProtocolError

class Agent(BaseModel, ABC):

    """
    Base AGENT class that stores general agent info, personality, and the task the agent
    is responsible for.

    Attributes:
        name (str): The name of the agent. Defaults to "Luminaria".
        model (str): The model or version the agent is based on. Defaults to "llama3.2/prometheus".
        instructions (Union[str, Callable[[], str]]): A set of instructions defining the agent's role
            or behavior. Can be a static string or a callable that returns a string.
        tendencies (Optional[Personality]): A Tendency object to define traits and adjust 
            the agent's responses and actions. Defaults to None.
        responsibilities (Optional[List[Callable[..., None]]]): A list of tasks or functions 
            the agent can execute. Defaults to an empty list.
        role (Literal["pilot","crew]): Determines the relationship of this agents to others, pilot
            being the leader/orchestrator, crew being just a worker agent

    Methods:
        run(**kwargs): Abstract method to be implemented by subclasses. This serves as the entry
            point for executing the agent's tasks and responsibilities.
    """

    name: str = "Luminaria",
    model: str = config.OLLAMA_MODEL_NAME,
    instructions: Union[str, Callable[[], str]] = "You are the light of the world.",
    tendencies: Optional[Tendencies] = None,
    role: Roles = "crew",
    communication_protocol: type[CommunicationProtocol] = None,
    status: str = "idle" # idle, running, awaiting_approval, completed



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Must Initialize the communication protocol
        self.communication_protocol = CommunicationProtocol(
            model=self.model,
            personality=self._build_personality(),
        )

    def _build_personality(self) -> str:
        """
        Combines instructions and tendecies to create a personality for this agent.
        """
        base_instructions = (
            self.instructions() if isinstance(self.instructions, callable) else self.instructions
        )
        tendencies_description = f"You're Tendecies are: {str(self.tendencies)}"
        return f"{base_instructions} : {tendencies_description}"


    async def prompt(self, message: str, sender: str = "user"):
        """Communication layer opened to talk to this agent."""
        try:
            res = await self.communication_protocol.send_prompt(message, sender=sender)
            return res
        except CommunicationsProtocolError as error:
            print(f"Error occured: {error.msg}, status_code: {error.status_code}")

    @abstractmethod
    async def task(self, **kwargs):
        """Abstract method to be implemented by subclasses. This is the method for determining the agent actions"""
        raise NotImplementedError()

    async def run(self, **kwargs):
        """
        Infinite execution loop for the agent. Delegates task-specific logic to `task` method.
        """
        while True:
            result = await self.task()
            yield result

            feedback = yield

            if feedback:
                result = await self.prompt(message=feedback, sender="pilot")
                yield result


