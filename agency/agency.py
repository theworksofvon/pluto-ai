import asyncio
from typing import List, Dict, Union, Optional
from .agent import Agent

class Agency:
    def __init__(self, agents: List[Agent]) -> None:
        self.agents: Dict[str, Agent] = {agent.name: agent for agent in agents}
        self.pilot = next((agent for agent in agents if agent.role == "pilot"), None)
        
        if not self.pilot:
            raise ValueError("Agency must have at least one pilot agent.")

    async def send_message(self, sender: str, message: str, receiver: Optional[str] = None) -> Union[str, None]:
        """
        Facilitates communication between agents.

        Args:
            sender (str): Name of the sending agent.
            receiver (str): Name of the receiving agent. Defaults to the pilot agent.
            message (str): Message to be sent.

        Returns:
            Union[str, None]: Response from the receiving agent, or None if the receiver is not found.
        """
        if receiver is not None and receiver not in self.agents:
            return f"Agent {receiver} not found in agency."
        if receiver is not None:
            agent = self.agents[receiver]
            res = await agent.prompt(message=message, sender=sender)
        elif receiver is None:
            res = await self.pilot.prompt(message=message, sender=sender)
        return res

    async def run(self):
        """
        Executes the tasks for all worker agents and facilitates communication with the pilot.
        Processes all worker agents concurrently.
        """

        async def process_agent(agent: Agent):
            if agent.role == "crew":
                print(f"Running task for worker agent: {agent.name}")

                max_iterations = 3
                feedback_iterations = 0
                async for result in agent.run():
                    print(f"Task result from {agent.name}: {result}")

                    feedback = await self.send_message(sender=agent.name, message=result)

                    # Send feedback to agent
                    await agent.run().asend(feedback)
                    feedback_iterations += 1

                    if feedback_iterations >= max_iterations:
                        break;

                return result

        tasks = [
            process_agent(agent=agent) for agent in self.agents.items() if agent.role == 'crew'
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return results
