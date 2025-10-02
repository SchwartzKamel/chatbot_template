"""Root agent module for the chatbot_template project.

This module defines the `root_agent` for ADK loader compatibility,
integrating with the Context7 MCP server for enhanced capabilities.
Environment configuration is loaded from `.env` and validated before agent initialization.
"""

import sys
import logging

import httpx
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv, dotenv_values

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Centralized environment variable loading
load_dotenv()
config = dotenv_values()

AZURE_API_KEY = config.get("AZURE_API_KEY")
AZURE_API_BASE = config.get("AZURE_API_BASE")
AZURE_API_VERSION = config.get("AZURE_API_VERSION")
AZURE_DEPLOYMENT_NAME = config.get("AZURE_DEPLOYMENT_NAME")

# Validate required environment variables
missing_vars = [
    var
    for var, value in {
        "AZURE_API_KEY": AZURE_API_KEY,
        "AZURE_API_BASE": AZURE_API_BASE,
        "AZURE_API_VERSION": AZURE_API_VERSION,
        "AZURE_DEPLOYMENT_NAME": AZURE_DEPLOYMENT_NAME,
    }.items()
    if not value
]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# Log non-sensitive configuration status
logger.info("Azure API configuration loaded successfully.")


def connect_to_context7_mcp(query: str = "test") -> dict:
    """Searches the Context7 MCP server for information based on a query.

    Args:
        query (str): The search query to send to the Context7 API.

    Returns:
        dict: Response data from the API or error information.
    """
    CONTEXT7_API_KEY = config.get("CONTEXT7_API_KEY")
    if not CONTEXT7_API_KEY:
        logger.error("Missing CONTEXT7_API_KEY environment variable.")
        return {
            "status": "error",
            "error_message": "Missing API key for Context7 MCP server.",
        }

    client = httpx.Client()
    try:
        headers = {"Authorization": f"Bearer {CONTEXT7_API_KEY}"}
        response = client.get(
            f"https://context7.com/api/v1/search?query={query}", headers=headers
        )
        if response.status_code == 200:
            search_results = response.json()
            logger.info("Successfully queried Context7 MCP server.")
            return {"status": "success", "results": search_results}
        else:
            logger.error(
                f"Failed to query Context7 MCP server. Status code: {response.status_code}"
            )
            return {
                "status": "error",
                "error_message": f"Failed with status code: {response.status_code}",
            }
    except Exception as e:
        logger.error(f"Error querying Context7 MCP server: {str(e)}")
        return {"status": "error", "error_message": str(e)}
    finally:
        client.close()


# Initialize connection to Context7 MCP server
context7_tools = connect_to_context7_mcp()
if context7_tools:
    logger.info(f"Available tools from Context7: {context7_tools}")
else:
    logger.warning("No tools loaded from Context7 MCP server.")

# Explicitly export root_agent so ADK can detect it
__all__ = ["root_agent"]

# Define individual agents for the multi-agent system
tool_runner = LlmAgent(
    name="ToolRunner",
    model=LiteLlm(
        model=f"azure/{AZURE_DEPLOYMENT_NAME}",  # LiteLLM Azure deployment name format
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    ),
    description="""
    Executes tools and specific functions on demand.
    Acts as the direct interface to connected utilities, APIs, and system calls.
    Designed for precision and reliability, ToolRunner ensures that every
    execution is logged, reproducible, and formatted for downstream use.
    Ideal for handling atomic operations, data retrieval, and context-sensitive
    actions that require deterministic outputs.
    
    Strengths:
      - Deterministic execution of tools
      - Clear, structured result formatting
      - Minimal overhead, optimized for speed
    Failure Modes:
      - Tool unavailable or misconfigured
      - Malformed input or unexpected output
      - Timeout or partial execution
    Recovery Strategies:
      - Retry with exponential backoff
      - Validate inputs before execution
      - Return structured error object for Orchestrator to handle
    """,
    instruction="""
    Role: Tool Execution Specialist
    Responsibilities:
      - Run assigned tools reliably
      - Process inputs and return structured outputs
      - Ensure results are formatted for downstream agents
    Constraints:
      - Do not self-delegate
      - Only use tools explicitly provided
    """,
    tools=[connect_to_context7_mcp],
)
# Create orchestrator agent and assign sub-agents
orchestrator = LlmAgent(
    name="Orchestrator",
    model=LiteLlm(
        model=f"azure/{AZURE_DEPLOYMENT_NAME}",  # LiteLLM Azure deployment name format
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    ),
    description="""
    Coordinates and manages tasks across multiple agents to achieve
    efficient, reliable outcomes. Functions as the central command layer,
    interpreting high-level goals and breaking them into actionable steps.
    Orchestrator ensures smooth collaboration between agents, resolves
    conflicts, and maintains global context across workflows.
    Optimized for scalability, adaptability, and balancing autonomy with oversight.
    
    Strengths:
      - Global context awareness
      - Dynamic task delegation
      - Conflict resolution and escalation
    Failure Modes:
      - Deadlock between sub-agents
      - Conflicting or redundant task assignments
      - Loss of context across long workflows
    Recovery Strategies:
      - Escalate unresolved tasks to human operator
      - Re-plan workflow with reduced scope
      - Request clarification or additional input
    """,
    instruction="""
    Role: Task Orchestrator
    Responsibilities:
      - Delegate tasks to specialized agents
      - Manage workflows and monitor progress
      - Integrate results into coherent outputs
    Constraints:
      - Avoid redundant execution
      - Escalate only when sub-agents cannot resolve
    Sub-agents:
      - ToolRunner
    """,
    sub_agents=[tool_runner],
)

# Set the root agent to be the orchestrator for ADK compatibility
root_agent = orchestrator
