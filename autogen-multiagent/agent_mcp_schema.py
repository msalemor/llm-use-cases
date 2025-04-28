import asyncio
from pathlib import Path
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken

from common import get_model_client


async def main() -> None:
    # Setup server params for local filesystem access
    server_params = StdioServerParams(
        command="/home/alex/.bun/bin/bun", args=["/home/alex/github/msalemor/llm-use-cases/autogen-multiagent/mcp-server/index.ts"]
    )

    # Get all available tools from the server
    tools = await mcp_server_tools(server_params)

    # Create an agent that can use all the tools
    agent = AssistantAgent(
        name="file_manager",
        model_client=get_model_client(),
        tools=tools,  # type: ignore
    )

    # The agent can now use any of the filesystem tools
    await agent.run(task="What is the schema for table events", cancellation_token=CancellationToken())


if __name__ == "__main__":
    asyncio.run(main())
