import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from common import get_model_client


model_client = get_model_client()


async def mock_get_icm_info(id: str):
    await asyncio.sleep(.1)
    return {
        "id": id,
        "title": "Too many 500 HTTP errors",
        "status": "pending",
        "priority": "high",
        "summary": "The service xyz is returning 500 HTTP errors out of expected SLA.",
    }


async def mock_kusto_query(id: str):
    await asyncio.sleep(.1)
    return [
        {"error": "500", "message": "unable to connect to database",
            "timestamp": "2023-10-01T12:00:00Z"},
        {"error": "500", "message": "unable to connect to database",
         "timestamp": "2023-10-01T12:00:00Z"},
    ]

icm_info = AssistantAgent(
    "get_icm_info",
    model_client,
    tools=[mock_get_icm_info],
    system_message="You are an AI that can get information about IT incidement management system.",
)

icm_classifier = AssistantAgent(
    "icm_classifier",
    model_client,
    system_message="""You are an AI that can classify a a text into one of the following labels:
- Infra: issues related to infrastructure or networking
- Change: issues related to change management or deployment
- App: issues related to application or software
- Security: issues related to security or compliance
- Unknown: issues that do not fit into any of the above categories

You will be provided with a text and you need to classify it into one of the above labels.
Provide the best classification label only in format:
```json
{
    "label": "<label>"
}
```
""",
)

kusto_query = AssistantAgent(
    "kusto_query",
    model_client,
    tools=[mock_kusto_query],
    system_message="""Get an analyze additional telemetry for the incident. Provide a summary of the findings.""",
)

rca_writer = AssistantAgent(
    "rca_writer",
    model_client,
    system_message="""Write a one paragraph IT incident management report including its classification. Provide possible root cause analysis causes and recommendations to avoid issue(s) in the future. After writing the report finisht with 'TERMINATE'""",
)

text_termination = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [icm_info, icm_classifier, kusto_query, rca_writer],
    termination_condition=text_termination
)


async def main():
    await Console(team.run_stream(
        task="ICM 1234",))

if __name__ == "__main__":
    asyncio.run(main())
