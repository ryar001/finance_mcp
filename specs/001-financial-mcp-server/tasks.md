---
description: "Task list for Financial MCP Server"
---

# Tasks: Financial MCP Server

**Input**: Design documents from `/specs/001-financial-mcp-server/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions.

## Path Conventions

- Paths shown below assume a single project structure (`src/`, `tests/`) as defined in `plan.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create project directories: `src/models`, `src/services`, `src/routers`, `tests/`
- [x] T002 Initialize Python environment and install dependencies using `uv pip install fastapi uvicorn python-dotenv pydantic pydantic_ai sqlmodel google-generativeai`
- [x] T003 Create a `.env` file in the project root for the `GEMINI_API_KEY`
- [x] T004 Set up the basic FastAPI application in `src/main.py`
- [x] T005 [P] Install testing framework with `uv pip install pytest`
- [x] T006 [P] Create a placeholder constants file in `src/services/const.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [x] T007 Implement the base LLM service configuration in `src/services/financial_data.py` using `pydantic_ai` and the Gemini API key from the `.env` file.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Retrieve Income Statement (Priority: P1) 🎯 MVP

**Goal**: As a developer, I want to be able to request an income statement for a specific company and receive it in a structured JSON format.

**Independent Test**: Call the `/income_statement` endpoint with a company name and verify the returned JSON matches the `IncomeStatement` model.

### Tests for User Story 1
- [x] T008 [P] [US1] Create unit test for the Income Statement model in `tests/test_models.py`
- [x] T009 [P] [US1] Create integration test for the `/income_statement` endpoint in `tests/test_routers.py` to check for valid responses.

### Implementation for User Story 1
- [x] T010 [US1] Create the `IncomeStatement` SQLModel in `src/models/income_statement.py` based on `data-model.md`.
- [x] T011 [US1] Implement the core `get_income_statement` function in `src/services/financial_data.py` to fetch and parse data into the `IncomeStatement` model.
- [x] T012 [US1] Create the API router in `src/routers/income_statement.py`.
- [x] T013 [US1] Implement the `GET /income_statement` endpoint in `src/routers/income_statement.py` that calls the service and returns JSON.
- [x] T014 [US1] Add the income statement router to the main FastAPI app in `src/main.py`.

**Checkpoint**: User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Retrieve Balance Sheet (Priority: P2)

**Goal**: As a developer, I want to be able to request a balance sheet for a specific company and receive it in a structured JSON format.

**Independent Test**: Call the `/balance_sheet` endpoint with a company name and verify the returned JSON matches the `BalanceSheet` model.

### Tests for User Story 2
- [ ] T015 [P] [US2] Create unit test for the Balance Sheet model in `tests/test_models.py`.
- [ ] T016 [P] [US2] Create integration test for the `/balance_sheet` endpoint in `tests/test_routers.py`.

### Implementation for User Story 2
- [ ] T017 [US2] Create the `BalanceSheet` SQLModel in `src/models/balance_sheet.py` based on `data-model.md`.
- [ ] T018 [US2] Implement the core `get_balance_sheet` function in `src/services/financial_data.py`.
- [ ] T019 [US2] Create the API router in `src/routers/balance_sheet.py`.
- [ ] T020 [US2] Implement the `GET /balance_sheet` endpoint in `src/routers/balance_sheet.py`.
- [ ] T021 [US2] Add the balance sheet router to the main FastAPI app in `src/main.py`.

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Retrieve Cash Flow Statement (Priority: P3)

**Goal**: As a developer, I want to be able to request a cash flow statement for a specific company and receive it in a structured JSON format.

**Independent Test**: Call the `/cash_flow_statement` endpoint with a company name and verify the returned JSON matches the `CashFlowStatement` model.

### Tests for User Story 3
- [ ] T022 [P] [US3] Create unit test for the Cash Flow Statement model in `tests/test_models.py`.
- [ ] T023 [P] [US3] Create integration test for the `/cash_flow_statement` endpoint in `tests/test_routers.py`.

### Implementation for User Story 3
- [ ] T024 [US3] Create the `CashFlowStatement` SQLModel in `src/models/cash_flow_statement.py` based on `data-model.md`.
- [ ] T025 [US3] Implement the core `get_cash_flow_statement` function in `src/services/financial_data.py`.
- [ ] T026 [US3] Create the API router in `src/routers/cash_flow_statement.py`.
- [ ] T027 [US3] Implement the `GET /cash_flow_statement` endpoint in `src/routers/cash_flow_statement.py`.
- [ ] T028 [US3] Add the cash flow statement router to the main FastAPI app in `src/main.py`.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T029 [P] Add comprehensive docstrings and inline comments to all new functions and models.
- [ ] T030 Implement centralized error handling in `src/main.py` for API errors or cases where data cannot be found.
- [ ] T031 Refactor shared logic in `src/services/financial_data.py` to improve code reuse.
- [ ] T032 Validate the complete implementation against `quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phase 3-5)**: Depend on Foundational phase completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2. No dependencies on other stories.
- **User Story 2 (P2)**: Can start after Phase 2. No dependencies on other stories.
- **User Story 3 (P3)**: Can start after Phase 2. No dependencies on other stories.

### Parallel Opportunities

- **Setup**: Tasks T005 and T006 can run in parallel.
- **User Stories**: Once the Foundational phase is complete, work on all User Stories (US1, US2, US3) can begin in parallel. Within each story, test creation can be parallelized.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently.

### Incremental Delivery

1.  Complete Setup + Foundational.
2.  Add User Story 1 → Test independently.
3.  Add User Story 2 → Test independently.
4.  Add User Story 3 → Test independently.
5.  Each story adds value without breaking previous stories.
