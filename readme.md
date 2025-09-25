# MCP Solution for Konsulent-Staffing

This project contains two FastAPI microservices:

1. **konsulent-api** – Provides a hardcoded list of consultants.
2. **mcp-llm-verktoy-api** – Fetches consultants from `konsulent-api`, filters them based on availability and skills, and generates a human-readable summary. Can optionally generate summaries using OpenRouter LLM. The service is built using FastMCP.
3. **llm-verktoy-api(Wrong solution)** - A previous attempt where I thought the case was building a simple REST API around LLM calls. This service is not used in the final solution.

Both services run in separate Docker containers and communicate over a Docker network.

## Requirements

- Docker
- Docker Compose
- `.env` file with your OpenRouter API key:

```env
OPENROUTER_API_KEY="sk-yourapikeyhere"
OPENROUTER_MODEL="yourmodelhere" # Optional, defaults to gpt-4o-mini
```

## Running the project

Start both services using Docker Compose:

```bash
docker-compose up --build
```

## Test endpoints

- Fetch all consultants:

  ```bash
  curl http://localhost:8000/konsulenter
  ```

- Get a summary of available consultants:

  ```bash
  curl "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&paakrevd_ferdighet=python"
  ```
