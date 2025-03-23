import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from common import get_creative_model_client


model_client = get_creative_model_client()


male_comedian = AssistantAgent(
    "Male_Comedian",
    model_client,
    system_message="You are a male comedian who is funny and witty. Finish by saying 'tell me a joke.'",
)

female_comedian = AssistantAgent(
    "Female_Comedian",
    model_client,
    system_message="You are a famale comedian who is a bit crass, funny, witty, and prefer jokes about 'why did the chicken cross the road and knock, knock'. Finish by saying 'tell me a joke.'",
)

text_termination = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [male_comedian, female_comedian],
    termination_condition=text_termination,
    max_turns=10)


async def main():
    await Console(team.run_stream(
        task="Tell me a joke",))

if __name__ == "__main__":
    asyncio.run(main())
