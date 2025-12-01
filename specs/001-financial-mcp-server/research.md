# Research: Financial MCP Server

## pydantic_ai for LLM Creation

- **Decision**: Use `pydantic_ai` for creating the LLM agent.
- **Rationale**: The user has explicitly requested this library. It simplifies the interaction with LLMs by allowing the definition of data structures that the LLM should return.
- **Alternatives considered**: None, as this was a direct requirement.

## SQLModel for Data Modeling

- **Decision**: Use `SQLModel` for defining the data models for the financial statements.
- **Rationale**: The user has explicitly requested this library. `SQLModel` is based on Pydantic and Python type hints, and it helps in creating data models that are both Pydantic models and SQLAlchemy models. Although we are not using the database features (`table=False`), it provides a strong and familiar way to define the data structure.
- **Alternatives considered**: None, as this was a direct requirement.

## FastAPI for MCP Server

- **Decision**: Use `FastAPI` to create the MCP server.
- **Rationale**: The constitution suggests `FastAPI` for building APIs. It is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Alternatives considered**: None, as this is the recommended framework.

## Gemini API for Web Search

- **Decision**: Use the Gemini API for web search.
- **Rationale**: The user has explicitly requested the use of Gemini. The Gemini API can be used for a variety of tasks, including web search, and it can be instructed to return structured data.
- **Alternatives considered**: None, as this was a direct requirement.
