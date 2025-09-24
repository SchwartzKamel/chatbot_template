"""Root agent module for the chatbot_template project.

This module defines the `root_agent` for ADK loader compatibility,
providing tools to answer questions about the time and weather in a city.
Environment configuration is loaded from `.env` and validated before agent initialization.
"""

import sys
import logging
import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

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


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


# Ensure root_agent is defined at module level for ADK loader
# ADK expects this exact variable at the top level of the module

# Explicitly export root_agent so ADK can detect it
__all__ = ["root_agent"]

# Removed duplicate environment variable loading here (already loaded above)

root_agent = LlmAgent(
    name="weather_time_agent",
    model=LiteLlm(
        model=f"azure/{AZURE_DEPLOYMENT_NAME}",  # LiteLLM Azure deployment name format
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    ),
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=("I can answer your questions about the time and weather in a city."),
    tools=[get_weather, get_current_time],
)
