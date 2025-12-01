# Research: MCP Financial Data Server

## pydantic_ai with Gemini

- **Structured Output:** Use Pydantic models to define the schema for the data you want to extract from Gemini. This is crucial for ensuring the data is in a predictable format.
- **Gemini's Native JSON Mode:** Leverage Gemini's native JSON mode to force the model to output a response that conforms to a specified JSON schema. The `google-generativeai` SDK simplifies this by allowing you to pass Pydantic models directly.
- **Pydantic AI Framework:** For more complex agentic workflows, the `pydantic-ai` framework is a good choice. It has built-in support for Gemini and simplifies the process of creating and managing AI agents.
- **Error Handling:** Implement robust error handling for API calls to Gemini, including retries for transient errors.

## langgraph for Orchestration

- **State Management:** Keep the state object minimal and explicitly typed using `TypedDict` or Pydantic. The state should be the single source of truth for the graph.
- **Modular Nodes:** Design nodes as small, single-responsibility functions that take the state as input and return a dictionary of updates.
- **Cycles:** LangGraph is well-suited for workflows that require cycles, such as retrying a tool call or refining a response.
- **Persistence:** For long-running or critical workflows, use a production-grade checkpointer like Postgres to persist the agent's state.
- **Parallel Execution:** Use parallel execution for independent nodes to speed up the workflow.

## Web Searches with Gemini for Financial Data

To get financial data from Gemini, you need to be specific in your prompts. For example, instead of asking for "financial data for Apple," you should ask for "the income statement for Apple for Q3 2025." You can also provide URLs to specific financial documents to guide the model.

## SQLModel with `table=False`

Setting `table=False` in a SQLModel model definition tells SQLModel not to create a database table for that model. This is useful for creating models that are used only for data validation and serialization, such as API request and response bodies.

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class EarningsStatementBase(SQLModel, table=False):
    income_statement: str
    balance_sheet: str
    cashflow_statement: str

class EarningsStatement(EarningsStatementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    period: str

class EarningsStatementCreate(EarningsStatementBase):
    pass

class EarningsStatementRead(EarningsStatementBase):
    id: int
    company: str
    period: str
```
