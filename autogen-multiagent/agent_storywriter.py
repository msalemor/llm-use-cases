

# Create the primary agent.
import asyncio

import click
from common import get_creative_model_client, get_model_client

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

from safedict import ThreadSafeDict

Story_writer = AssistantAgent(
    "Story_writer",
    model_client=get_creative_model_client(),
    system_message="You are a very creative children book author. Keep the stories short. If revising the story, write the full story with the revisions.",
)

# Create the critic agent.
Story_reviewer = AssistantAgent(
    "Story_reviewer",
    model_client=get_model_client(),
    system_message="You are a helpful AI assistant which provides constructive feedback on Kids stories to add a postive impactful ending. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

# Define a termination condition that stops the task if the critic approves.
text_termination = TextMentionTermination("APPROVE")

# Create a team with the primary and critic agents.

# Define the main asynchronous function


# Replace the sessions dictionary with a thread-safe dictionary
sessions = ThreadSafeDict()


async def process(sessionid: str, task: str) -> None:
    team = RoundRobinGroupChat(
        [Story_writer, Story_reviewer], termination_condition=text_termination)
    res = team.run_stream(task=task)
    # await Console(res)  # Stream the messages to the console.
    async for message in res:
        # print(message)
        if isinstance(message, str):
            print("String message:", message)
        elif hasattr(message, "content"):
            if hasattr(message, "source"):
                # print("Message role:", message.role)
                click.echo(click.style(message.source +
                           "\n", fg='yellow', bold=True))
            # print("Message content:", message.content)
            print(message.content + "\n")
        else:
            # print("Other message type:", message)
            sessions.set(sessionid, message)
            try:
                msg = message.messages[-1]
                print(msg)
            except Exception as e:
                pass


async def main():
    t1 = process("jdoe", "Write a story about a dog living in the moon.")
    t2 = process("mdoe", "Write a story a cat in the city.")
    await asyncio.gather(t1, t2)
    print(sessions.items())

    # Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(main())
