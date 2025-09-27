"""Root agent module for the chatbot_template project.

This module defines the `root_agent` for ADK loader compatibility,
integrating with the Context7 MCP server for enhanced capabilities.
Environment configuration is loaded from `.env` and validated before agent initialization.
"""

import sys
import logging

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables once
load_dotenv()

# Centralized environment variable loading
from dotenv import dotenv_values

# Centralized environment variable loading without os.getenv
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
        return {"status": "error", "error_message": "Missing API key for Context7 MCP server."}
    
    client = httpx.Client()
    try:
        headers = {"Authorization": f"Bearer {CONTEXT7_API_KEY}"}
        response = client.get(f"https://context7.com/api/v1/search?query={query}", headers=headers)
        if response.status_code == 200:
            search_results = response.json()
            logger.info("Successfully queried Context7 MCP server.")
            return {"status": "success", "results": search_results}
        else:
            logger.error(f"Failed to query Context7 MCP server. Status code: {response.status_code}")
            return {"status": "error", "error_message": f"Failed with status code: {response.status_code}"}
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

# Ensure root_agent is defined at module level for ADK loader
# ADK expects this exact variable at the top level of the module

# Explicitly export root_agent so ADK can detect it
__all__ = ["root_agent"]

# Removed duplicate environment variable loading here (already loaded above)

# Define individual agents for the multi-agent system
tool_runner = LlmAgent(
    name="ToolRunner",
    model=LiteLlm(
        model=f"azure/{AZURE_DEPLOYMENT_NAME}",  # LiteLLM Azure deployment name format
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    ),
    description="I am responsible for running tools and executing specific functions.",
    instruction="I can execute tools and provide results as needed.",
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
    description="I coordinate tasks across multiple agents for efficient operation.",
    instruction="I manage and delegate tasks to specialized agents.",
    sub_agents=[tool_runner]
)

# Set the root agent to be the orchestrator for ADK compatibility
root_agent = orchestrator
