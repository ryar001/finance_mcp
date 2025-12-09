#!/usr/bin/env python3
"""
Live test script for the financial data service.
This script tests the actual Gemini API websearch functionality.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from finance_mcp.services.financial_data import get_income_statement, list_available_models


async def main():
    print("=" * 80)
    print("LIVE API TEST - Financial Data Service")
    print("=" * 80)
    print()
    
    # Test 1: List available models
    print("Test 1: Listing available Gemini models...")
    print("-" * 80)
    try:
        await list_available_models()
        print("✅ Successfully listed available models")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    print()
    print("=" * 80)
    
    # Test 2: Get income statement for Apple
    print("Test 2: Fetching income statement for Apple Inc.")
    print("-" * 80)
    try:
        company = "Apple Inc."
        print(f"Requesting income statement for: {company}")
        print("This may take a few seconds as the LLM performs a web search...")
        print()
        
        # Enable more verbose logging temporarily
        import logging
        logging.basicConfig(level=logging.DEBUG)
        
        income_statement = await get_income_statement(company)
        
        if income_statement:
            print("✅ Successfully retrieved income statement!")
            print()
            print("Income Statement Data:")
            print("-" * 80)
            print(f"  Revenue:                ${income_statement.revenue:,.2f}")
            print(f"  Cost of Goods Sold:     ${income_statement.cost_of_goods_sold:,.2f}")
            print(f"  Gross Profit:           ${income_statement.gross_profit:,.2f}")
            print(f"  Operating Expenses:     ${income_statement.operating_expenses:,.2f}")
            print(f"  Operating Income:       ${income_statement.operating_income:,.2f}")
            print(f"  Non-Operating Income:   ${income_statement.non_operating_income:,.2f}")
            print(f"  Pre-Tax Income:         ${income_statement.pre_tax_income:,.2f}")
            print(f"  Income Tax Expense:     ${income_statement.income_tax_expense:,.2f}")
            print(f"  Net Income:             ${income_statement.net_income:,.2f}")
            print("-" * 80)
        else:
            print("❌ Failed to retrieve income statement (returned None)")
            print("Check the logs directory for more details")
    except Exception as e:
        print(f"❌ Error fetching income statement: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    
    # Test 3: Get income statement for Microsoft
    print("Test 3: Fetching income statement for Microsoft Corporation")
    print("-" * 80)
    try:
        company = "Microsoft Corporation"
        print(f"Requesting income statement for: {company}")
        print("This may take a few seconds as the LLM performs a web search...")
        print()
        
        income_statement = await get_income_statement(company)
        
        if income_statement:
            print("✅ Successfully retrieved income statement!")
            print()
            print("Income Statement Data:")
            print("-" * 80)
            print(f"  Revenue:                ${income_statement.revenue:,.2f}")
            print(f"  Cost of Goods Sold:     ${income_statement.cost_of_goods_sold:,.2f}")
            print(f"  Gross Profit:           ${income_statement.gross_profit:,.2f}")
            print(f"  Operating Expenses:     ${income_statement.operating_expenses:,.2f}")
            print(f"  Operating Income:       ${income_statement.operating_income:,.2f}")
            print(f"  Non-Operating Income:   ${income_statement.non_operating_income:,.2f}")
            print(f"  Pre-Tax Income:         ${income_statement.pre_tax_income:,.2f}")
            print(f"  Income Tax Expense:     ${income_statement.income_tax_expense:,.2f}")
            print(f"  Net Income:             ${income_statement.net_income:,.2f}")
            print("-" * 80)
        else:
            print("❌ Failed to retrieve income statement (returned None)")
    except Exception as e:
        print(f"❌ Error fetching income statement: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("LIVE API TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
