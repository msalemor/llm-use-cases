import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
import click

from common import get_model_client


async def main() -> None:
    model_client = get_model_client()

    async def lookup_hotel(location: str) -> str:
        return f"Here are some hotels in {location}: hotel1, hotel2, hotel3."

    async def lookup_flight(origin: str, destination: str) -> str:
        return f"Here are some flights from {origin} to {destination}: flight1, flight2, flight3."

    async def book_trip() -> str:
        return "Your trip is booked!"

    travel_advisor = AssistantAgent(
        "Travel_Advisor",
        model_client,
        tools=[book_trip],
        description="Helps with travel planning.",
    )

    hotel_agent = AssistantAgent(
        "Hotel_Agent",
        model_client,
        tools=[lookup_hotel],
        description="Helps with hotel booking.",
    )

    flight_agent = AssistantAgent(
        "Flight_Agent",
        model_client,
        tools=[lookup_flight],
        description="Helps with flight booking.",
    )

    termination = TextMentionTermination("TERMINATE")
    team = SelectorGroupChat(
        [travel_advisor, hotel_agent, flight_agent],
        model_client=model_client,
        termination_condition=termination,
    )

    # await Console(team.run_stream(task="Book a 3-day trip to new york."))
    res = team.run_stream(task="Book a 3-day trip to new york.")
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
            if isinstance(message.content, str):
                print(message.content + "\n")
            else:
                print(type(message.content))

        else:
            # print("Other message type:", message)
            pass


if __name__ == "__main__":
    # Run the main function using asyncio.
    # This is necessary because the main function is asynchronous.
    # If you don't want to use asyncio.run, you can also use asyncio.get_event_loop().run_until_complete(main())
    # or create an event loop and run the main function in it.
    asyncio.run(main())
