"""
Realistic demonstration data generator for FinPlot AI.
Generates isolated, labeled sample transactions for demonstration and testing.
All records have is_demo = True so they are strictly separated from live user records.
"""

from datetime import date, timedelta
from typing import Any, Dict, List


def get_demo_transactions() -> List[Dict[str, Any]]:
    """
    Returns a curated set of realistic business transactions spanning recent months.
    Useful for demonstrating dashboard metrics, cash flow trends, and category breakdowns.
    """
    today = date.today()

    def d(days_ago: int) -> str:
        return (today - timedelta(days=days_ago)).isoformat()

    return [
        # --- Income Transactions ---
        {
            "transaction_date": d(3),
            "description": "Acme Corp — Enterprise SaaS Annual License",
            "amount": 12500.00,
            "transaction_type": "income",
            "category": "Sales Revenue",
            "payment_method": "Bank Transfer",
            "notes": "Annual enterprise subscription invoice #INV-2026-081",
            "is_demo": True,
        },
        {
            "transaction_date": d(12),
            "description": "Stripe Payout — Monthly E-Commerce Sales",
            "amount": 4820.50,
            "transaction_type": "income",
            "category": "Sales Revenue",
            "payment_method": "Stripe",
            "notes": "Net payout after processing fees",
            "is_demo": True,
        },
        {
            "transaction_date": d(20),
            "description": "Nexus Labs — AI Architecture Retainer",
            "amount": 6000.00,
            "transaction_type": "income",
            "category": "Consulting",
            "payment_method": "Wire",
            "notes": "Milestone 2 consulting completion",
            "is_demo": True,
        },
        {
            "transaction_date": d(38),
            "description": "Stripe Payout — Monthly Subscriptions",
            "amount": 5150.00,
            "transaction_type": "income",
            "category": "Sales Revenue",
            "payment_method": "Stripe",
            "notes": "Recurring tier-1 customer billing",
            "is_demo": True,
        },
        {
            "transaction_date": d(45),
            "description": "Vanguard Treasury Yield Payout",
            "amount": 340.20,
            "transaction_type": "income",
            "category": "Investment Return",
            "payment_method": "Bank Transfer",
            "notes": "Monthly operational treasury yield",
            "is_demo": True,
        },
        {
            "transaction_date": d(65),
            "description": "Apex Digital — Mobile App Dev Contract",
            "amount": 9500.00,
            "transaction_type": "income",
            "category": "Client Invoicing",
            "payment_method": "Bank Transfer",
            "notes": "Final handover acceptance",
            "is_demo": True,
        },
        {
            "transaction_date": d(80),
            "description": "Stripe Payout — Quarterly Starter Tier",
            "amount": 3950.00,
            "transaction_type": "income",
            "category": "Sales Revenue",
            "payment_method": "Stripe",
            "notes": "Automated recurring batch",
            "is_demo": True,
        },
        # --- Expense Transactions ---
        {
            "transaction_date": d(2),
            "description": "Amazon Web Services (AWS) — Cloud Hosting",
            "amount": 845.60,
            "transaction_type": "expense",
            "category": "Cloud & Infrastructure",
            "payment_method": "Credit Card",
            "notes": "EC2 clusters, RDS PostgreSQL, S3 buckets",
            "is_demo": True,
        },
        {
            "transaction_date": d(5),
            "description": "Google Workspace & GCP Cloud Console",
            "amount": 168.00,
            "transaction_type": "expense",
            "category": "Software & SaaS",
            "payment_method": "Credit Card",
            "notes": "12 user seats + cloud logging quota",
            "is_demo": True,
        },
        {
            "transaction_date": d(8),
            "description": "GitHub Enterprise & Copilot Business",
            "amount": 210.00,
            "transaction_type": "expense",
            "category": "Software & SaaS",
            "payment_method": "Credit Card",
            "notes": "Engineering team toolchain license",
            "is_demo": True,
        },
        {
            "transaction_date": d(15),
            "description": "WeWork Shared Office Space Rent",
            "amount": 2200.00,
            "transaction_type": "expense",
            "category": "Rent & Real Estate",
            "payment_method": "Bank Transfer",
            "notes": "Monthly dedicated 6-desk team space",
            "is_demo": True,
        },
        {
            "transaction_date": d(18),
            "description": "Senior Backend Contractor (Upwork)",
            "amount": 3400.00,
            "transaction_type": "expense",
            "category": "Salaries & Contractor",
            "payment_method": "Wire",
            "notes": "API performance optimization sprint",
            "is_demo": True,
        },
        {
            "transaction_date": d(22),
            "description": "Meta & LinkedIn Ads Acquisition Campaign",
            "amount": 1450.00,
            "transaction_type": "expense",
            "category": "Marketing & Advertising",
            "payment_method": "Credit Card",
            "notes": "Q1 B2B customer acquisition campaign",
            "is_demo": True,
        },
        {
            "transaction_date": d(30),
            "description": "Accounting & Tax Compliance Filing",
            "amount": 750.00,
            "transaction_type": "expense",
            "category": "Legal & Accounting",
            "payment_method": "Bank Transfer",
            "notes": "Quarterly sales tax and bookkeeping review",
            "is_demo": True,
        },
        {
            "transaction_date": d(35),
            "description": "Amazon Web Services (AWS) — Cloud Hosting",
            "amount": 810.40,
            "transaction_type": "expense",
            "category": "Cloud & Infrastructure",
            "payment_method": "Credit Card",
            "notes": "Production clusters",
            "is_demo": True,
        },
        {
            "transaction_date": d(42),
            "description": "WeWork Shared Office Space Rent",
            "amount": 2200.00,
            "transaction_type": "expense",
            "category": "Rent & Real Estate",
            "payment_method": "Bank Transfer",
            "notes": "Monthly dedicated desk space",
            "is_demo": True,
        },
        {
            "transaction_date": d(50),
            "description": "Figma & Adobe Creative Cloud Subscription",
            "amount": 145.00,
            "transaction_type": "expense",
            "category": "Software & SaaS",
            "payment_method": "Credit Card",
            "notes": "Product design and UI asset licensing",
            "is_demo": True,
        },
        {
            "transaction_date": d(70),
            "description": "TechStars Summit Flights & Hotel Lodging",
            "amount": 1120.00,
            "transaction_type": "expense",
            "category": "Travel & Entertainment",
            "payment_method": "Credit Card",
            "notes": "Investor presentation travel expenses",
            "is_demo": True,
        },
        {
            "transaction_date": d(75),
            "description": "High-Speed Business Fiber Internet",
            "amount": 135.00,
            "transaction_type": "expense",
            "category": "Utilities & Internet",
            "payment_method": "Debit Card",
            "notes": "1 Gbps dedicated office connection",
            "is_demo": True,
        },
    ]
