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
    def __init__(self):
        # Agents share context **THIS IS IMPORTANT**
        self.shared_context: List[Message] = []
        self.system_prompt = ""

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
    def __init__(self, name: str, system: str | None = None):
        super().__init__()
        self.name = name
        self.system_prompt = system


book_author = Agent(
    "book_author", system="You are an AI children book author. Given a title create a fun and inspiring short story.")
book_reviewer = Agent(
    "book_reviewer", system="You are an children author book editor. Given a story, provide feedback and suggestions for improvement including ending with a moral.")
agent_list: List[BaseAgent] = [book_author, book_reviewer]


async def runner(task: str):
    # Note: sharing messages between agents
    # this is key as the message context is shared between agents
    messages = [Message(agent="user", role="user",
                        content=task, ts=datetime.now())]
    for agent in agent_list:
        # run the agent
        context = await agent.process(messages=messages)
        messages = context
    messages.append(
        Message(agent="runner", role="runner", content="Done", ts=datetime.now()))
    print("Final context:")
    for message in messages:
        print(f"{message.agent} <-> {message.role}:\n{message.content}")


if __name__ == "__main__":
    asyncio.run(runner(task="Write a story about a cat"))
