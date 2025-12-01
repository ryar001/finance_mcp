# Feature Specification: Financial MCP Server

**Feature Branch**: `001-financial-mcp-server`  
**Created**: 2025-12-01
**Status**: Draft  
**Input**: User description: "create a financial mcp server that enable llm to pull financial data -the mcp server should be be wrapper for a function that does the main job and the mcp is another function that wrap this function -create a mcp function for income, balance sheet and cashflow statement -it will call a llm(gemini) to websearch for the data needed -output a sqlModel object with table =False from the function - and the mcp function should convert it to json and return the data -use pydantic_ai for llm creation -the keys will be in .env at project root -if need to install package, use uv add"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve Income Statement (Priority: P1)

As a developer, I want to be able to request an income statement for a specific company and receive it in a structured JSON format.

**Why this priority**: This is a core feature of the financial data server.

**Independent Test**: This can be tested by calling the income statement MCP function with a company name and verifying that the returned JSON is well-formed and contains the correct data.

**Acceptance Scenarios**:

1. **Given** a valid company name, **When** the income statement MCP function is called, **Then** a JSON object containing the income statement is returned.
2. **Given** an invalid company name, **When** the income statement MCP function is called, **Then** an error message is returned.

---

### User Story 2 - Retrieve Balance Sheet (Priority: P2)

As a developer, I want to be able to request a balance sheet for a specific company and receive it in a structured JSON format.

**Why this priority**: This is a core feature of the financial data server.

**Independent Test**: This can be tested by calling the balance sheet MCP function with a company name and verifying that the returned JSON is well-formed and contains the correct data.

**Acceptance Scenarios**:

1. **Given** a valid company name, **When** the balance sheet MCP function is called, **Then** a JSON object containing the balance sheet is returned.
2. **Given** an invalid company name, **When** the balance sheet MCP function is called, **Then** an error message is returned.

---

### User Story 3 - Retrieve Cash Flow Statement (Priority: P3)

As a developer, I want to be able to request a cash flow statement for a specific company and receive it in a structured JSON format.

**Why this priority**: This is a core feature of the financial data server.

**Independent Test**: This can be tested by calling the cash flow statement MCP function with a company name and verifying that the returned JSON is well-formed and contains the correct data.

**Acceptance Scenarios**:

1. **Given** a valid company name, **When** the cash flow statement MCP function is called, **Then** a JSON object containing the cash flow statement is returned.
2. **Given** an invalid company name, **When** the cash flow statement MCP function is called, **Then** an error message is returned.

---

### Edge Cases

- What happens when the web search returns no results?
- How does the system handle malformed or unexpected data from the web search?
- What happens if the Gemini API is unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an MCP (Managed Component Port) server.
- **FR-002**: The server MUST expose separate MCP functions for retrieving income statements, balance sheets, and cash flow statements.
- **FR-003**: Each MCP function MUST wrap a core function that performs the main data retrieval logic.
- **FR-004**: The core function MUST use an LLM (Gemini) to perform a web search for the required financial data.
- **FR-005**: The core function MUST parse the web search results and structure the data into a `SQLModel` object with `table=False`.
- **FR-006**: The MCP function MUST convert the `SQLModel` object into a JSON object before returning it.
- **FR-007**: The LLM creation MUST be handled by the `pydantic_ai` library.
- **FR-008**: API keys and other secrets MUST be loaded from a `.env` file at the project root.
- **FR-009**: Any new package installations MUST be performed using the `uv add` command.

### Key Entities *(include if feature involves data)*

- **IncomeStatement**: Represents the financial data for an income statement.
- **BalanceSheet**: Represents the financial data for a balance sheet.
- **CashFlowStatement**: Represents the financial data for a cash flow statement.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A request to the income statement MCP function for a valid company returns a JSON object containing the correct income statement data within 10 seconds.
- **SC-002**: A request to the balance sheet MCP function for a valid company returns a JSON object containing the correct balance sheet data within 10 seconds.
- **SC-003**: A request to the cash flow statement MCP function for a valid company returns a JSON object containing the correct cash flow statement data within 10 seconds.
- **SC-004**: A request for a non-existent company or for a statement that cannot be found returns a clear and informative error message.