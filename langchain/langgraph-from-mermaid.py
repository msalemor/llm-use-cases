import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool, BaseTool
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
import json


# Configuration
@dataclass
class Config:
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
    api_version: str = "2024-02-01"
    kusto_cluster: str = os.getenv("KUSTO_CLUSTER", "")
    kusto_database: str = os.getenv("KUSTO_DATABASE", "")
    kusto_app_id: str = os.getenv("KUSTO_APP_ID", "")
    kusto_app_key: str = os.getenv("KUSTO_APP_KEY", "")
    kusto_tenant_id: str = os.getenv("KUSTO_TENANT_ID", "")


# Initialize configuration
config = Config()

# Initialize Azure OpenAI
llm = AzureChatOpenAI(
    azure_endpoint=config.azure_endpoint,
    api_key=config.api_key,
    deployment_name=config.deployment_name,
    api_version=config.api_version,
    temperature=0,
)

# Initialize Kusto client
kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    config.kusto_cluster,
    config.kusto_app_id,
    config.kusto_app_key,
    config.kusto_tenant_id,
)
kusto_client = KustoClient(kcsb)


# Tools for KQL Agent
class GetSchemaToolByTableName(BaseTool):
    name = "get_schema_by_table"
    description = "Get the schema of a KQL table by its name"

    def _run(self, table_name: str) -> str:
        try:
            query = f".show table {table_name} schema as json"
            response = kusto_client.execute(config.kusto_database, query)

            for row in response.primary_results[0]:
                schema_json = json.loads(row[0])
                return json.dumps(schema_json, indent=2)
        except KustoServiceError as e:
            return f"Error getting schema: {str(e)}"

    async def _arun(self, table_name: str) -> str:
        return self._run(table_name)


class KQLExecutionTool(BaseTool):
    name = "execute_kql_query"
    description = "Execute a KQL query and return the results"

    def _run(self, query: str) -> str:
        try:
            response = kusto_client.execute(config.kusto_database, query)
            results = []

            for row in response.primary_results[0]:
                results.append(list(row))

            return json.dumps(
                {
                    "columns": [
                        col.column_name for col in response.primary_results[0].columns
                    ],
                    "data": results[:100],  # Limit to first 100 rows
                },
                indent=2,
            )
        except KustoServiceError as e:
            return f"Error executing query: {str(e)}"

    async def _arun(self, query: str) -> str:
        return self._run(query)


# Create tools
get_schema_tool = GetSchemaToolByTableName()
execute_kql_tool = KQLExecutionTool()

# Create KQL ReAct Agent
kql_tools = [get_schema_tool, execute_kql_tool]

kql_agent_prompt = PromptTemplate.from_template(
    """You are a KQL (Kusto Query Language) expert agent.
Your task is to:
1. Identify the tables involved in the user's natural language query
2. Get the schema for those tables
3. Generate an appropriate KQL query based on the schema and user request
4. Execute the query and return the results

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
)

kql_agent = create_react_agent(llm, kql_tools, kql_agent_prompt)
kql_agent_executor = AgentExecutor(agent=kql_agent, tools=kql_tools, verbose=True)


# Report Generator Agent
def report_generator_agent(query_results: Dict[str, Any], original_query: str) -> str:
    """Generate a summary report from KQL query results"""
    system_prompt = """You are a data analyst expert. Your task is to generate a clear, 
    concise summary report from KQL query results. Focus on key insights and patterns."""

    user_prompt = f"""Original Query: {original_query}

Query Results:
{json.dumps(query_results, indent=2)}

Please generate a summary report highlighting the key findings and insights from this data."""

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    response = llm.invoke(messages)
    return response.content


# Define state for LangGraph
class AgentState(dict):
    query: str
    kql_results: Optional[Dict[str, Any]] = None
    report: Optional[str] = None
    error: Optional[str] = None


# Master Agent workflow using LangGraph
def create_master_agent_workflow():
    workflow = StateGraph(AgentState)

    # Define nodes
    def process_kql_query(state: AgentState) -> AgentState:
        """Process the query using KQL Agent"""
        try:
            result = kql_agent_executor.invoke({"input": state["query"]})
            # Parse the result to extract the query results
            if "output" in result:
                try:
                    state["kql_results"] = json.loads(result["output"])
                except:
                    state["kql_results"] = {"raw_output": result["output"]}
            return state
        except Exception as e:
            state["error"] = str(e)
            return state

    def generate_report(state: AgentState) -> AgentState:
        """Generate report from KQL results"""
        if state.get("kql_results") and not state.get("error"):
            state["report"] = report_generator_agent(
                state["kql_results"], state["query"]
            )
        return state

    # Add nodes
    workflow.add_node("kql_agent", process_kql_query)
    workflow.add_node("report_generator", generate_report)

    # Define edges
    workflow.set_entry_point("kql_agent")
    workflow.add_edge("kql_agent", "report_generator")
    workflow.add_edge("report_generator", END)

    return workflow.compile()


# Main application
def main():
    # Create the master agent workflow
    master_agent = create_master_agent_workflow()

    # Example usage
    query = "Show me the top 10 events from the last 24 hours"

    # Run the workflow
    initial_state = AgentState(query=query)
    result = master_agent.invoke(initial_state)

    # Display results
    if result.get("error"):
        print(f"Error: {result['error']}")
    else:
        print(f"Query: {result['query']}")
        print(f"\nKQL Results: {json.dumps(result.get('kql_results', {}), indent=2)}")
        print(f"\nReport:\n{result.get('report', 'No report generated')}")


if __name__ == "__main__":
    main()
