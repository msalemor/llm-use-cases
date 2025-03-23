import asyncio
from typing import Dict, Any, List


from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import Swarm
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination

from common import get_model_client


simple_classifier_agent = AssistantAgent(
    "classifier_agent",
    model_client=get_model_client(),
    system_message="""You are a classifier agent. Given a text use the following classification tabels:
    - Change management: issues related to change management and/or deployment.
    - Security: issues related to security.
    - Application: issues related to application such as bugs and/on unexpected behavior.
    - Unknown: issues that cannot be classified into any of the above categories.
    Return the best classification label only. No epilogue or prologue.""",
)


async def classify(task: str) -> str:
    resp = await simple_classifier_agent.run(task=task)
    return resp.messages[-1].content


async def classifier(text: str) -> str:
    """Classify the IM details"""
    return "Infrastructure and networking"


async def mock_get_kusto_data(id, database=None, table=None, query=None):
    await asyncio.sleep(.1)  # Simulate a network call
    return {"id": id, "status": "pending", "summary": "Unable to connect to application with Azure Front Door.", "classification": "TBD"}


async def get_IM(id: str) -> Dict[str, Any]:
    """Get stock market data for a given symbol"""
    return await mock_get_kusto_data(id)

planner = AssistantAgent(
    "planner",
    model_client=get_model_client(),
    handoffs=["IM_details_agent", "classifier_agent", "writer"],
    system_message="""You are an incident management (IM) root cause (RCA) analyzer.
    Anlyze the IM and find the root cause analysis by using using the following specialized agents:
    - IM Extractor: Get the IM information
    - Classifier: Classify IM information
    - Writer: For compiling final IM RCA report
    Always send your plan first, then handoff to appropriate agent.
    Always handoff to a single agent at a time.
    Use TERMINATE when analysis is complete.""",
)

kql_planner = AssistantAgent(
    "kql_planner",
    model_client=get_model_client(),
    handoffs=["IM_details_agent", "classifier_agent", "writer"],
    system_message="""You are an incident management (IM) root cause analysis (RCA) tool.
    Find the root cause analysis by using using the following specialized agents:
    - IM Extractor: Get the IM information
    - Classifier: Classify IM information 
    - Writer: For compiling final IM RCA report
    Always send your plan first, then handoff to appropriate agent.
    Always handoff to a single agent at a time.
    Use TERMINATE when analysis is complete.""",
)


IM_details_agent = AssistantAgent(
    "IM_details_agent",
    model_client=get_model_client(),
    handoffs=["planner"],
    tools=[get_IM],
    system_message="""You are an incident management (IM) details extraction tool.
    Extract IM and provide details using the get_IM tool.
    Always handoff back to planner when extraction is complete.""",
)

classifier_agent = AssistantAgent(
    "classifier_agent",
    model_client=get_model_client(),
    handoffs=["planner"],
    system_message="""You are an agent that can classify an incident management. The classification labels are:
    - Infrastructure and networking: issues related to infrastructure and/or networking.
    - Change management: issues related to change management and/or deployment.
    - Security: issues related to security.
    - Application: issues related to application such as bugs and/on unexpected behavior.
    - Unknown: issues that cannot be classified into any of the above categories.
    Classify IM details and return the best classification label.
    Output format:
    Classification: < classification label >
    Always handoff back to planner when classification is complete.""",
)

writer_agent = AssistantAgent(
    "writer",
    model_client=get_model_client(),
    handoffs=["planner"],
    system_message="""You are an root cause (RCA) report writer.    
    Gather the IM information and classification label and generate a concise RCA report. Use the following output format:

    \"\"\"text
    IM ID: < IM ID >
    IM Classification: < IM Classification >
    IM Status: < IM Status >
    IM Summary:
    < IM Summary >
    Root Cause Analysis:
    < RCA >
    \"\"\"
    
    Always handoff back to planner when writing is complete.
    Use TERMINATE when writing is complete.""",
)

# Define termination condition
text_termination = TextMentionTermination("TERMINATE")
termination = text_termination
research_team = Swarm(
    participants=[planner, IM_details_agent, classifier_agent,
                  writer_agent], termination_condition=termination
)


async def rca_analysis(task: str) -> None:
    task_result = await Console(research_team.run_stream(task=task))
    print(task_result)

if __name__ == "__main__":
    # Example task
    asyncio.run(rca_analysis("What is the root cause of the IM 12345?"))
