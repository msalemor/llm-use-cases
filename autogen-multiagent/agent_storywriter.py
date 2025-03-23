

# Create the primary agent.
import asyncio

import click
from common import get_creative_model_client, get_model_client

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

Story_writer = AssistantAgent(
    "Story_writer",
    model_client=get_creative_model_client(),
    system_message="You are a children book author. Keep the stories short",
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
team = RoundRobinGroupChat(
    [Story_writer, Story_reviewer], termination_condition=text_termination)

# Define the main asynchronous function


async def main():
    # await Console(
    #     team.run_stream(task="Write a story about a dog living in the moon.")
    # )  # Stream the messages to the console.
    res = team.run_stream(task="Write a story about a dog living in the moon.")
    async for message in res:
        # print(message)
        if isinstance(message, str):
            # print("String message:", message)
            pass
        elif hasattr(message, "content"):
            if hasattr(message, "source"):
                # print("Message role:", message.role)
                click.echo(click.style(message.source +
                           "\n", fg='yellow', bold=True))
            # print("Message content:", message.content)
            print(message.content + "\n")
        else:
            # print("Other message type:", message)
            pass

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(main())
