# Chatbot Template

A minimal Python-based chatbot agent compatible with the **ADK loader**.  
This template demonstrates basic agent functionality that integrates with the Context7 MCP server for enhanced capabilities.

## Prerequisites

- **Python**: 3.12 or later
- **ADK** (Agent Development Kit) installed
- **Docker** (optional, for containerized deployment)
- Dependencies listed in `pyproject.toml`

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd chatbot_template
   ```

2. **Create a `.env` file**:
   - Copy `example.env` to `.env`
   - Fill in the required environment variables (see below)
   ```bash
   cp example.env .env
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Run the chatbot**:
   ```bash
   adk web
   ```

## Quickstart with Docker

For a fast setup and deployment using Docker, fill out the .env, then use the provided Makefile command:

```bash
make auto-cache
```

This command builds the Docker image with cache for quicker subsequent builds and runs the container using Docker Compose.

## Environment Variables

The following variables **must** be set in `.env`:

- `AZURE_API_KEY` — Azure API key
- `AZURE_API_BASE` — Azure API base URL
- `AZURE_API_VERSION` — Azure API version
- `AZURE_DEPLOYMENT_NAME` — Azure deployment name
- `CONTEXT7_API_KEY` — (Optional) API key for Context7 MCP server integration

> **Note**: Do **not** commit your `.env` file or share sensitive values.
