import os
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

# Debug logging to verify environment variables
print(f"[DEBUG] AZURE_API_KEY loaded: {'SET' if AZURE_API_KEY else 'NOT SET'}")
print(f"[DEBUG] AZURE_API_BASE loaded: {AZURE_API_BASE}")
print(f"[DEBUG] AZURE_API_VERSION loaded: {AZURE_API_VERSION}")
print(f"[DEBUG] AZURE_DEPLOYMENT_NAME loaded: {AZURE_DEPLOYMENT_NAME}")


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

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

root_agent = LlmAgent(
    name="weather_time_agent",
    model=LiteLlm(
        model=f"azure/{AZURE_DEPLOYMENT_NAME}",  # LiteLLM Azure deployment name format
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION
    ),
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=("I can answer your questions about the time and weather in a city."),
    tools=[get_weather, get_current_time],
)
