import os

import click
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from langchain import hub

load_dotenv()
llm = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version=os.getenv("OPENAI_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("OPENAI_GPT_DEPLOYMENT", "gpt-4o"),
)

# react_prompt_template = """
# Answer the following questions as best you can. You have access to the following tools:

# {tools}

# Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}
# """

react_prompt = hub.pull("hwchase17/react")
print(react_prompt.template)


async def addition(x: str) -> str:
    """Adds two numbers together."""
    parts = x.split(",")
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError(
            "Invalid input for addition. Expected two numbers separated by a comma."
        )
    return str(int(parts[0]) + int(parts[1]))


async def subtraction(x: str) -> str:
    """Subtracts the second number from the first."""
    parts = x.split(",")
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError(
            "Invalid input for subtraction. Expected two numbers separated by a comma."
        )
    return str(int(parts[0]) - int(parts[1]))


async def multiplication(x: str) -> str:
    """Multiplies two numbers together."""
    parts = x.split(",")
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError(
            "Invalid input for multiplication. Expected two numbers separated by a comma."
        )
    return str(int(parts[0]) * int(parts[1]))


async def division(x: str) -> str:
    """Divides the first number by the second."""
    parts = x.split(",")
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError(
            "Invalid input for division. Expected two numbers separated by a comma."
        )
    if int(parts[1]) == 0:
        raise ValueError("Division by zero is not allowed.")
    return str(int(x.split(",")[0]) / int(x.split(",")[1]))


async def main():
    tools = [
        StructuredTool.from_function(
            coroutine=addition,
            name="addition",
            description="Adds two numbers together.",
        ),
        StructuredTool.from_function(
            coroutine=subtraction,
            name="subtraction",
            description="Subtracts the second number from the first.",
        ),
        StructuredTool.from_function(
            coroutine=multiplication,
            name="multiplication",
            description="Multiplies two numbers together.",
        ),
        StructuredTool.from_function(
            coroutine=division,
            name="division",
            description="Divides the first number by the second.",
        ),
    ]

    prompt = ChatPromptTemplate.from_template(react_prompt.template)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
        # callbacks=callbacks,
    )
    result = await agent_executor.ainvoke(
        {"input": "What is 5 * 2, plus 10, divided by 2?"},
        # config={"callbacks": callbacks},
    )

    click.echo(click.style(result, fg="cyan"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    # main()
