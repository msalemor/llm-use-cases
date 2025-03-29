import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import List, Protocol
from dataclasses_json import dataclass_json

from common import completion


@dataclass_json
@dataclass
class Message:
    agent: str
    role: str
    content: str
    ts: datetime


class BaseAgent:
    """
    BaseAgent is a foundational class for creating agents that share a common context and interact with a system prompt.
    Attributes:
        name (str | None): The name of the agent. Defaults to None.
        shared_context (List[Message]): A shared list of messages that represents the agent's context.
        system_prompt (str | None): The system prompt associated with the agent. Defaults to None.
    Methods:
        __init__():
            Initializes the BaseAgent with default values for name, shared_context, and system_prompt.
        switch_context(context):
            Updates the shared context by replacing the existing system prompt (if any) with the current system prompt.
        async process(task: str | None = None, messages: List[Message] = None):
            Processes a task by updating the shared context, appending the task as a user message, and calling the LLM for a response.
        serialized_messages() -> List[dict]:
            Serializes the shared context messages into a list of dictionaries for further processing.
    Notes:
        - The shared_context attribute is critical as it allows agents to maintain a shared state across interactions.
        - The system_prompt is dynamically updated in the shared context to reflect the agent's current state.
    """

    def __init__(self):
        # Agents share context **THIS IS IMPORTANT**
        self.name: str | None = None
        self.shared_context: List[Message] = []
        self.system_prompt: str | None = None

    def switch_context(self, context):
        # if the agent share_context has a systm prompt already, remove it, and add the current system prompt as first one on the list
        if self.shared_context and self.shared_context[0].role == "system":
            self.shared_context.pop(0)
        if self.system_prompt:
            self.shared_context.insert(
                0, Message(agent=self.name, role="system", content=self.system_prompt, ts=datetime.now()))

    async def process(self, task: str | None = None, messages: List[Message] = None):
        print(f"Agent: {self.name}")
        self.shared_context = messages if messages else []

        # Switch system message based on agent
        self.switch_context(self.system_prompt)

        if task:
            self.shared_context.append(
                Message(agent=self.name, role="user", content=task, ts=datetime.now()))

        # Call the LLM
        result = await completion(self.serialized_messages())

        # add result to context
        self.shared_context.append(
            Message(agent=self.name, role="user", content=result, ts=datetime.now()))

        return self.shared_context

    def serialized_messages(self) -> List[dict]:
        serializable_messages = [message.to_dict()
                                 for message in self.shared_context]
        return serializable_messages


class Agent(BaseAgent):
    """
    Represents an agent in a multi-agent system.
    This class extends the BaseAgent class and is designed to encapsulate 
    the behavior and attributes of an individual agent. Each agent has a 
    unique name and an optional system prompt that can be used to define 
    its behavior or context.
    Attributes:
        name (str): The name of the agent, used to uniquely identify it.
        system_prompt (str | None): An optional system prompt that provides 
            context or instructions for the agent's behavior.
    Methods:
        __init__(name: str, system: str | None = None):
            Initializes the Agent instance with a name and an optional 
            system prompt.
    """

    def __init__(self, name: str, system: str | None = None):
        super().__init__()
        self.name = name
        self.system_prompt = system


class AgentManager:
    """
    Runner AgentManager
    The `AgentManager` class is responsible for managing and executing a sequence of agents in a pipeline. 
    It facilitates the registration of agents and orchestrates the processing of tasks through 
    a shared message context. Each agent in the pipeline modifies the shared context, enabling 
    collaborative task execution.
    Attributes:
        agent_list (List[BaseAgent]): A list of agents registered to the runner. Each agent is 
        expected to implement an asynchronous `process` method.
    Methods:
        register(agent: BaseAgent):
            Registers an agent to the runner's agent list.
        process(task: str):
            Executes the registered agents in sequence, sharing a common message context. 
            Each agent processes the task and updates the context, which is passed to the next agent.
    """

    def __init__(self):
        self.agent_list: List[BaseAgent] = []

    def register(self, agent: BaseAgent):
        """
        Registers an agent in the agent list.
        Args:
            agent (BaseAgent): The agent to be registered.
        """
        self.agent_list.append(agent)

    async def process(self, task: str):
        """
        Executes a sequence of agents in a pipeline, sharing a common message context.
        This function takes a task description as input and processes it through a list of agents.
        Each agent modifies the shared message context, which is then passed to the next agent in the sequence.
        Finally, a "Done" message is appended to the context, and the resulting messages are printed.
        Args:
            task (str): The intial task to be processed by the agents.
        Notes:
            - The `messages` list is used to share context between agents.
            - Each agent in `agent_list` is expected to have an asynchronous `process` method that takes
            the current `messages` as input and returns the updated context.
            - The function appends a final message indicating completion before printing the context.
        Example:
            >>> await runner("Translate this text")
        """

        # Note: sharing messages between agents
        # this is key as the message context is shared between agents
        messages = [Message(agent="user", role="user",
                            content=task, ts=datetime.now())]
        for agent in self.agent_list:
            # run the agent
            context = await agent.process(messages=messages)
            messages = context
        messages.append(
            Message(agent="runner", role="runner", content="Done", ts=datetime.now()))
        print("Final context:")
        for message in messages:
            print(f"{message.agent} <-> {message.role}:\n{message.content}")


async def main():
    runner = AgentManager()

    # Create two agents
    book_author = Agent(
        "book_author", system="You are an AI children book author. Given a title create a fun and inspiring short story.")
    book_reviewer = Agent(
        "book_reviewer", system="You are an children author book editor. Given a story, provide feedback and suggestions for improvement including ending with a moral.")

    runner.register(book_author)
    runner.register(book_reviewer)

    await runner.process(
        "Write a story about a cosmopolitan cat living in NYC.")

if __name__ == "__main__":

    asyncio.run(main())
