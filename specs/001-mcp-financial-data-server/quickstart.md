# Quickstart: MCP Financial Data Server

This guide will show you how to get the earnings statement for a company using the MCP Financial Data Server.

## Get an Earnings Statement

To get an earnings statement, you need to send a POST request to the `/earnings_statement` endpoint with the company name and the time period.

### Request

Here's an example of how to make the request using `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/earnings_statement' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company": "Apple",
  "period": "Q3 2025"
}'
```

### Response

The server will respond with a JSON object containing the earnings statement for the company.

```json
{
  "id": 1,
  "company": "Apple",
  "period": "Q3 2025",
  "income_statement": "...",
  "balance_sheet": "...",
  "cashflow_statement": "..."
}
```

