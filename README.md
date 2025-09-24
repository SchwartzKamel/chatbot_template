# Chatbot Template

A minimal Python-based chatbot agent compatible with the **ADK loader**.  
This template demonstrates basic agent functionality with static demo outputs for weather and time queries.

## Prerequisites

- **Python**: 3.9 or later
- **ADK** (Agent Development Kit) installed
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

## Environment Variables

The following variables **must** be set in `.env`:

- `AZURE_API_KEY` — Azure API key
- `AZURE_API_BASE` — Azure API base URL
- `AZURE_API_VERSION` — Azure API version
- `AZURE_DEPLOYMENT_NAME` — Azure deployment name

> **Note**: Do **not** commit your `.env` file or share sensitive values.

## Usage

Once running, the chatbot responds to:
- `get_weather` — Returns static weather data for New York.
- `get_current_time` — Returns the current time in New York.

Example:
```plaintext
User: What's the weather in New York?
Bot: The weather in New York is sunny, 25°C.
```

## Limitations

- Weather and time data are **static** and only for **New York**.
- No dynamic API integration for real-time data.
- Single-threaded, synchronous execution.

## Future Improvements

- Integrate live weather and time APIs.
- Support multiple cities and dynamic queries.
- Add asynchronous execution for better performance.
- Implement automated tests.

---