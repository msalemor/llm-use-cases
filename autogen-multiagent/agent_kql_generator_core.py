import asyncio
import json
from dataclasses import dataclass
from typing import List

from autogen_core import (
    AgentId,
    CancellationToken,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    message_handler,
)
from autogen_core.models import (
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import FunctionTool, Tool
from autogen_core.models import AssistantMessage, FunctionExecutionResult, FunctionExecutionResultMessage, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient


@dataclass
class Message:
    content: str


@dataclass
class Message:
    content: str


schema_extractor_topic_type = "SchemaExtractorAgent"
kql_generator_topic_type = "KQLGeneratorAgent"


class ToolUseAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient, tool_schema: List[Tool]) -> None:
        super().__init__("An agent with tools")
        self._system_messages: List[LLMMessage] = [
            SystemMessage(content="You are a helpful AI assistant.")]
        self._model_client = model_client
        self._tools = tool_schema

    @message_handler
    async def handle_user_message(self, message: Message, ctx: MessageContext) -> Message:
        # Create a session of messages.
        session: List[LLMMessage] = self._system_messages + \
            [UserMessage(content=message.content, source="user")]

        # Run the chat completion with the tools.
        create_result = await self._model_client.create(
            messages=session,
            tools=self._tools,
            cancellation_token=ctx.cancellation_token,
        )

        # If there are no tool calls, return the result.
        if isinstance(create_result.content, str):
            return Message(content=create_result.content)
        assert isinstance(create_result.content, list) and all(
            isinstance(call, FunctionCall) for call in create_result.content
        )

        # Add the first model create result to the session.
        session.append(AssistantMessage(
            content=create_result.content, source="assistant"))

        # Execute the tool calls.
        results = await asyncio.gather(
            *[self._execute_tool_call(call, ctx.cancellation_token) for call in create_result.content]
        )

        # Add the function execution results to the session.
        session.append(FunctionExecutionResultMessage(content=results))

        # Run the chat completion again to reflect on the history and function execution results.
        create_result = await self._model_client.create(
            messages=session,
            cancellation_token=ctx.cancellation_token,
        )
        assert isinstance(create_result.content, str)

        # Return the result as a message.
        return Message(content=create_result.content)

    async def _execute_tool_call(
        self, call: FunctionCall, cancellation_token: CancellationToken
    ) -> FunctionExecutionResult:
        # Find the tool by name.
        tool = next(
            (tool for tool in self._tools if tool.name == call.name), None)
        assert tool is not None

        # Run the tool and capture the result.
        try:
            arguments = json.loads(call.arguments)
            result = await tool.run_json(arguments, cancellation_token)
            return FunctionExecutionResult(
                call_id=call.id, content=tool.return_value_as_string(result), is_error=False, name=tool.name
            )
        except Exception as e:
            return FunctionExecutionResult(call_id=call.id, content=str(e), is_error=True, name=tool.name)

# import asyncio

# from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.conditions import TextMentionTermination
# from autogen_agentchat.ui import Console
# from autogen_agentchat.teams import RoundRobinGroupChat
# from common import get_model_client


# model_client = get_model_client()


# async def mock_get_schema(name: str) -> dict:
#     await asyncio.sleep(.1)
#     if name == "logs":
#         return {
#             "cluster": "loggingevents",
#             "database": "logs",
#             "table": "events",
#             "fields": "id (string),userid (string), ts (timestamp), event (string), systemid (string), type (string)",
#             "description": "This table provides information about login events.\ntypes: infra, code, app, security, change",
#         }
#     if name == "users":
#         return {
#             "cluster": "loggingevents",
#             "database": "logs",
#             "table": "users",
#             "fields": "userid (string), name (string)",
#             "description": "This table provides information about users.",
#         }
#     if name == "system":
#         return {
#             "cluster": "master",
#             "database": "services",
#             "table": "systems",
#             "fields": "systemid (string), name (string), ha (boolean)",
#             "description": "this table provides system information.",
#         }
#     return {}


# get_schema = AssistantAgent(
#     "get_schema",
#     model_client,
#     tools=[mock_get_schema],
#     system_message="""You are an AI that can get the table or function KQL schema. There are 3 main objects you can use to get the schema:
# logs: system events related to systems and users
# users: user information
# system: system information
# """,
# )

# gen_kql_query = AssistantAgent(
#     "gen_kql_query",
#     model_client,
#     system_message="""You are an AI that can generate a KQL queries based on the schema provided.
# If the cluster and database names are provided, use them in the generated query.
# Example with cluster and database name:
# cluster('name').database('table').events | where ts>ago(24h)

# Once generate write 'TERMINATE'.\n""",
# )

# text_termination = TextMentionTermination("TERMINATE")

# team = RoundRobinGroupChat(
#     [get_schema, gen_kql_query],
#     termination_condition=text_termination
# )


# async def main():
#     await Console(team.run_stream(
#         task="Write a query to find all events by user name and system name in the last 24 hours?",))

# if __name__ == "__main__":
#     asyncio.run(main())
