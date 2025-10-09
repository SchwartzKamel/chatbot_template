import asyncio
import logging

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.devui import serve
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv, dotenv_values

# Centralized environment variable loading
load_dotenv()
config = dotenv_values()

AZURE_AI_PROJECT_ENDPOINT = config.get("AZURE_AI_PROJECT_ENDPOINT")
if not AZURE_AI_PROJECT_ENDPOINT:
    raise ValueError(
        "AZURE_AI_PROJECT_ENDPOINT is not set in the environment variables."
    )
AZURE_AI_MODEL_DEPLOYMENT_NAME = config.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")
if not AZURE_AI_MODEL_DEPLOYMENT_NAME:
    raise ValueError(
        "AZURE_AI_MODEL_DEPLOYMENT_NAME is not set in the environment variables."
    )

agent = ChatAgent(
    name="Joker Agent",
    chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
    instructions="You are good at telling jokes.",
)


async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting Joker Agent...")
    
    serve(entities=[agent])


if __name__ == "__main__":
    asyncio.run(main())
