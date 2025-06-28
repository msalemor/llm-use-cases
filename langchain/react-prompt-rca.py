import os
import json
from datetime import datetime, timedelta

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

# Sample ticket data (simulating a ticket system)
TICKET_DATA = {
    "INC001": {
        "title": "Unable to login to cloud portal",
        "description": "Users are reporting they cannot login to the cloud portal. Getting 'Authentication failed' error.",
        "priority": "High",
        "created": "2025-06-28T09:00:00Z",
        "affected_users": 150,
        "status": "Open",
    },
    "INC002": {
        "title": "Application performance degradation",
        "description": "Web application is running slowly, page load times increased from 2s to 15s.",
        "priority": "Critical",
        "created": "2025-06-28T08:30:00Z",
        "affected_users": 500,
        "status": "Open",
    },
    "INC003": {
        "title": "Database connection timeouts",
        "description": "Multiple services reporting database connection timeouts and failed queries.",
        "priority": "Critical",
        "created": "2025-06-28T10:15:00Z",
        "affected_users": 200,
        "status": "Open",
    },
}

# Sample infrastructure data
INFRASTRUCTURE_DATA = {
    "servers": [
        {
            "name": "web-server-01",
            "status": "healthy",
            "cpu": 25,
            "memory": 60,
            "last_restart": "2025-06-27T02:00:00Z",
        },
        {
            "name": "web-server-02",
            "status": "degraded",
            "cpu": 85,
            "memory": 90,
            "last_restart": "2025-06-25T14:30:00Z",
        },
        {
            "name": "db-server-01",
            "status": "critical",
            "cpu": 95,
            "memory": 95,
            "last_restart": "2025-06-28T09:30:00Z",
        },
        {
            "name": "auth-server-01",
            "status": "down",
            "cpu": 0,
            "memory": 0,
            "last_restart": "2025-06-28T08:45:00Z",
        },
    ],
    "networks": [
        {
            "name": "prod-network",
            "status": "healthy",
            "latency": "15ms",
            "packet_loss": "0.1%",
        },
        {
            "name": "db-network",
            "status": "degraded",
            "latency": "85ms",
            "packet_loss": "2.5%",
        },
    ],
}

# Sample change management data
CHANGE_DATA = [
    {
        "change_id": "CHG001",
        "title": "Database schema update",
        "implemented": "2025-06-28T08:00:00Z",
        "type": "Database",
        "risk": "Medium",
        "rollback_available": True,
    },
    {
        "change_id": "CHG002",
        "title": "Authentication service update",
        "implemented": "2025-06-28T07:30:00Z",
        "type": "Security",
        "risk": "High",
        "rollback_available": True,
    },
    {
        "change_id": "CHG003",
        "title": "Load balancer configuration change",
        "implemented": "2025-06-27T20:00:00Z",
        "type": "Infrastructure",
        "risk": "Low",
        "rollback_available": False,
    },
]

# Sample security events
SECURITY_DATA = [
    {
        "event_id": "SEC001",
        "type": "Failed Authentication",
        "count": 1500,
        "timestamp": "2025-06-28T09:00:00Z",
        "source_ips": ["192.168.1.100", "10.0.0.50"],
        "severity": "High",
    },
    {
        "event_id": "SEC002",
        "type": "Certificate Expiration Warning",
        "count": 1,
        "timestamp": "2025-06-28T06:00:00Z",
        "details": "SSL certificate for auth.company.com expires in 2 days",
        "severity": "Medium",
    },
]

rca_prompt_template = """
You are a Root Cause Analysis (RCA) expert for cloud-based services. Your job is to investigate incidents and determine the root cause.

You have access to the following tools to gather information:

{tools}

Use the following format for your investigation:

Question: the incident you need to investigate
Thought: you should always think about what information you need to gather
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now have enough information to determine the root cause
Final Answer: Provide a comprehensive RCA report including:
1. INCIDENT SUMMARY
2. ROOT CAUSE CATEGORY (Change Management, Infrastructure, Security, or Other)
3. DETAILED ROOT CAUSE
4. IMPACT ASSESSMENT
5. IMMEDIATE ACTIONS TAKEN
6. PREVENTIVE MEASURES
7. TIMELINE OF EVENTS

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""


async def get_ticket_details(ticket_id: str) -> str:
    """Retrieves detailed information about a specific incident ticket."""
    if ticket_id in TICKET_DATA:
        ticket = TICKET_DATA[ticket_id]
        return json.dumps(ticket, indent=2)
    else:
        return f"Ticket {ticket_id} not found. Available tickets: {list(TICKET_DATA.keys())}"


async def get_infrastructure_status(component: str = "all") -> str:
    """Gets the current status of infrastructure components (servers, networks, etc.)."""
    if component == "all":
        return json.dumps(INFRASTRUCTURE_DATA, indent=2)
    elif component in INFRASTRUCTURE_DATA:
        return json.dumps(INFRASTRUCTURE_DATA[component], indent=2)
    else:
        return f"Component '{component}' not found. Available components: {list(INFRASTRUCTURE_DATA.keys())}"


async def get_recent_changes(hours: str = "24") -> str:
    """Retrieves recent changes implemented in the specified number of hours."""
    try:
        hours_int = int(hours)
        cutoff_time = datetime.now() - timedelta(hours=hours_int)

        recent_changes = []
        for change in CHANGE_DATA:
            change_time = datetime.fromisoformat(
                change["implemented"].replace("Z", "+00:00")
            )
            if change_time.replace(tzinfo=None) >= cutoff_time:
                recent_changes.append(change)

        return json.dumps(recent_changes, indent=2)
    except ValueError:
        return "Invalid hours parameter. Please provide a number."


async def get_security_events(event_type: str = "all") -> str:
    """Retrieves security events and alerts from the monitoring system."""
    if event_type == "all":
        return json.dumps(SECURITY_DATA, indent=2)
    else:
        filtered_events = [
            event
            for event in SECURITY_DATA
            if event_type.lower() in event["type"].lower()
        ]
        return json.dumps(filtered_events, indent=2)


async def analyze_logs(service: str, pattern: str = "") -> str:
    """Simulates log analysis for a specific service looking for error patterns."""
    # Simulated log analysis results
    log_analysis = {
        "auth-service": {
            "error_count": 1500,
            "common_errors": [
                "Authentication failed: Invalid credentials",
                "Database connection timeout",
                "SSL handshake failed",
            ],
            "error_spike_time": "2025-06-28T09:00:00Z",
        },
        "web-service": {
            "error_count": 250,
            "common_errors": [
                "Database query timeout",
                "Connection pool exhausted",
                "HTTP 503 Service Unavailable",
            ],
            "error_spike_time": "2025-06-28T08:30:00Z",
        },
        "database": {
            "error_count": 800,
            "common_errors": [
                "Connection timeout",
                "Lock wait timeout exceeded",
                "Too many connections",
            ],
            "error_spike_time": "2025-06-28T08:00:00Z",
        },
    }

    if service in log_analysis:
        result = log_analysis[service]
        if pattern:
            # Filter logs by pattern
            filtered_errors = [
                error
                for error in result["common_errors"]
                if pattern.lower() in error.lower()
            ]
            result["filtered_errors"] = filtered_errors
        return json.dumps(result, indent=2)
    else:
        return f"Service '{service}' not found. Available services: {list(log_analysis.keys())}"


async def check_dependencies(service: str) -> str:
    """Checks the status of dependencies for a specific service."""
    dependencies = {
        "auth-service": {
            "database": "critical - connection timeout",
            "active_directory": "healthy",
            "certificate_store": "warning - certificate expiring soon",
            "load_balancer": "healthy",
        },
        "web-service": {
            "database": "critical - high latency",
            "auth-service": "down",
            "cache_service": "degraded",
            "cdn": "healthy",
        },
        "database": {
            "storage": "degraded - high I/O wait",
            "backup_service": "healthy",
            "monitoring": "healthy",
        },
    }

    if service in dependencies:
        return json.dumps(dependencies[service], indent=2)
    else:
        return f"Service '{service}' not found. Available services: {list(dependencies.keys())}"


async def main():
    tools = [
        StructuredTool.from_function(
            coroutine=get_ticket_details,
            name="get_ticket_details",
            description="Retrieves detailed information about a specific incident ticket.",
        ),
        StructuredTool.from_function(
            coroutine=get_infrastructure_status,
            name="get_infrastructure_status",
            description="Gets the current status of infrastructure components (servers, networks, etc.).",
        ),
        StructuredTool.from_function(
            coroutine=get_recent_changes,
            name="get_recent_changes",
            description="Retrieves recent changes implemented in the specified number of hours.",
        ),
        StructuredTool.from_function(
            coroutine=get_security_events,
            name="get_security_events",
            description="Retrieves security events and alerts from the monitoring system.",
        ),
        StructuredTool.from_function(
            coroutine=analyze_logs,
            name="analyze_logs",
            description="Simulates log analysis for a specific service looking for error patterns.",
        ),
        StructuredTool.from_function(
            coroutine=check_dependencies,
            name="check_dependencies",
            description="Checks the status of dependencies for a specific service.",
        ),
    ]

    prompt = ChatPromptTemplate.from_template(rca_prompt_template)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )

    # Example RCA investigation
    result = await agent_executor.ainvoke(
        {
            "input": "Investigate incident INC001 - users unable to login to cloud portal. Perform a comprehensive root cause analysis."
        },
    )

    click.echo(click.style("=== ROOT CAUSE ANALYSIS REPORT ===", fg="green", bold=True))
    click.echo(click.style(result["output"], fg="cyan"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


# ### Root Cause Analysis Report: Incident INC001

# #### 1. INCIDENT SUMMARY
# - **Title**: Unable to login to cloud portal
# - **Description**: Users experienced authentication failures while trying to log in to the cloud portal. Error messages included "Authentication failed," "Database connection timeout," and "SSL handshake failed."
# - **Reported Time**: 2025-06-28T09:00:00Z
# - **Affected Users**: 150
# - **Priority**: High

# #### 2. ROOT CAUSE CATEGORY
# - **Category**: Change Management

# #### 3. DETAILED ROOT CAUSE
# The incident was caused by the combined effects of two recent changes:
# - **CHG001 - Database schema update**: This change introduced database connection issues, including timeouts and lock wait timeouts, that disrupted interactions between the database and the "auth-service."
# - **CHG002 - Authentication service update**: This high-risk update exposed the database issues within the authentication workflow, leading to widespread user login failures.

# Additionally, a warning regarding expiring SSL certificates in the certificate store may have contributed to SSL handshake errors, but was not the primary driver of the incident.

# #### 4. IMPACT ASSESSMENT
# - **User Impact**: 150 users were unable to log in, disrupting access to critical services.
# - **Service Impact**: Authentication service functionality was severely degraded, causing failures across the cloud portal.
# - **Business Impact**: Customer trust and operations were affected due to high-priority service downtime.

# #### 5. IMMEDIATE ACTIONS TAKEN
# - Rolled back CHG002 ("Authentication service update") to restore previous authentication functionality.
# - Restarted the database service and increased connection limits to mitigate immediate database issues.
# - Notified stakeholders about the expiring SSL certificate and initiated an emergency renewal process.

# #### 6. PREVENTIVE MEASURES
# - Implement rigorous testing of database schema changes in pre-production environments to simulate all dependent workflows.
# - Enhance monitoring and alerting systems for post-change evaluations to detect anomalies immediately after implementation.
# - Require scheduled certificate audits and automated renewal processes to avoid unforeseen SSL issues.
# - Conduct a risk review for high-priority changes to evaluate interdependencies before implementation.

# #### 7. TIMELINE OF EVENTS
# - **2025-06-27T20:00:00Z**: CHG003 ("Load balancer configuration change") implemented.
# - **2025-06-28T07:30:00Z**: CHG002 ("Authentication service update") implemented.
# - **2025-06-28T08:00:00Z**: CHG001 ("Database schema update") implemented. Database logs show a spike in errors.
# - **2025-06-28T09:00:00Z**: User authentication failures reported. Incident ticket INC001 created.
# - **2025-06-28T10:00:00Z**: Root cause identified; immediate rollback and mitigation actions taken.
# - **2025-06-28T11:00:00Z**: Service functionality restored.
