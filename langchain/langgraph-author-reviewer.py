import os

import click
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from typing import TypedDict, Literal
from dotenv import load_dotenv


# Define the state
class DocumentState(TypedDict):
    topic: str
    document: str
    feedback: str
    status: Literal["draft", "review", "approved"]


# Initialize Azure OpenAI LLM

load_dotenv()
llm = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version=os.getenv("OPENAI_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("OPENAI_GPT_DEPLOYMENT", "gpt-4o"),
)


# Author agent
def author_node(state: DocumentState) -> DocumentState:
    click.echo(click.style(f"Author: {state}", fg="yellow"))
    if state["status"] == "draft":
        prompt = f"Write a detailed technical document on the topic: {state['topic']}."
    else:
        prompt = f"Revise the following document based on this feedback:\n\nFeedback: {state['feedback']}\n\nDocument:\n{state['document']}"

    response = llm.invoke(
        [
            SystemMessage(content="You are a technical writer."),
            HumanMessage(content=prompt),
        ]
    )

    return {**state, "document": response.content, "status": "review"}


# Reviewer agent
def reviewer_node(state: DocumentState) -> DocumentState:
    click.echo(click.style(f"Reviewer: {state}", fg="cyan"))
    prompt = f"Review the following technical document and provide constructive feedback. If it's good, say 'APPROVED'.\n\nDocument:\n{state['document']}"

    response = llm.invoke(
        [
            SystemMessage(content="You are a technical reviewer."),
            HumanMessage(content=prompt),
        ]
    )

    feedback = response.content
    status = "approved" if "APPROVED" in feedback.upper() else "draft"

    return {**state, "feedback": feedback, "status": status}


# Conditional router
def route(state: DocumentState) -> str:
    click.echo(click.style(f"Route: {state}", fg="yellow"))
    return END if state["status"] == "approved" else "author"


# Build the graph
builder = StateGraph(DocumentState)
builder.add_node("author", author_node)
builder.add_node("reviewer", reviewer_node)
builder.set_entry_point("author")
builder.add_edge("author", "reviewer")
builder.add_conditional_edges("reviewer", route)

graph = builder.compile()

# LangGraph can create a visual representation of the graph
graph.get_graph().draw_mermaid_png(output_file_path="author_reviewer_graph.png")

# Run the graph
topic = "Quantum Computing and Qubits"
final_state = graph.invoke(
    {"topic": topic, "document": "", "feedback": "", "status": "draft"}
)

click.echo(click.style(f"Final Document:\n{final_state['document']}", fg="green"))
click.echo(click.style(f"\nFinal Feedback:\n{final_state['feedback']}", fg="magenta"))
