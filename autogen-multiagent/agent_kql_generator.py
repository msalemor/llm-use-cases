import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from common import get_model_client


model_client = get_model_client()


async def mock_get_schema(name: str) -> dict:
    await asyncio.sleep(.1)
    if name == "logs":
        return {
            "cluster": "loggingevents.contoso.com",
            "database": "logs",
            "table": "events",
            "fields": "id (string),userid (string), ts (timestamp), event (string), systemid (string), type (string)",
            "description": "This table provides information about login events.\ntypes: infra, code, app, security, change",
        }
    if name == "users":
        return {
            "cluster": "loggingevents.contoso.com",
            "database": "logs",
            "table": "users",
            "fields": "userid (string), name (string)",
            "description": "This table provides information about users.",
        }
    if name == "system":
        return {
            "cluster": "master.contoso.com",
            "database": "services",
            "table": "systems",
            "fields": "systemid (string), name (string), ha (boolean)",
            "description": "this table provides system information.",
        }
    return {}


get_schema = AssistantAgent(
    "get_schema",
    model_client,
    tools=[mock_get_schema],
    system_message="""You are an AI that can get the table or function KQL schema. There are 3 main objects you can use to get the schema:
logs: system events related to systems and users
users: user information
system: system information
""",
)

gen_kql_query = AssistantAgent(
    "gen_kql_query",
    model_client,
    system_message="""You are an AI that can generate a KQL queries based on the schema provided. 
If the cluster and database names are provided, use them in the generated query. 
Example with cluster and database name: 
cluster('name.domain.com').database('table').events | where ts>ago(24h)

Once generate write 'TERMINATE'.\n""",
)

text_termination = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [get_schema, gen_kql_query],
    termination_condition=text_termination
)


async def process_agent_messages(task: str):
    res = team.run_stream(task=task)
    print(f"Task:\n{task}\n")
    async for message in res:
        if isinstance(message, str):
            # print("String message:", message)
            pass
        elif hasattr(message, "content"):
            # if hasattr(message, "source"):
            #     # print("Message role:", message.role)
            #     click.echo(click.style(message.source +
            #                "\n", fg='yellow', bold=True))
            # # print("Message content:", message.content)
            # print(message.content + "\n")
            pass
        else:
            # print("Other message type:", message)
            try:
                print("Result:")
                print(message.messages[-1].content)
                print()
            except Exception as e:
                pass


async def main():
    # await Console(team.run_stream(
    #     task="Find all the infra events in the last 1 hour",))
    await process_agent_messages(task="Find all the infra events in the last 1 hour")
    await process_agent_messages(task="Find all the codes events in the last 1 hour. Show the user name.")
    await process_agent_messages(task="Write a query to find all events by user name and system name in the last 24 hours")

if __name__ == "__main__":
    asyncio.run(main())
