#!/usr/bin/env python
"""
PromptCraft - Database Initialization Script

Creates all tables and runs migrations.
Usage: python -m scripts.init_db
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.session import engine, Base
from app.models import (
    User,
    Lesson,
    LessonProgress,
    Puzzle,
    PuzzleAttempt,
    UserGamification,
    XPTransaction,
    Badge,
    UserBadge,
    DailyChallenge,
    UserDailyChallenge
)


async def init_database():
    """Initialize database with all tables."""
    print("🚀 Initializing PromptCraft database...")

    async with engine.begin() as conn:
        # Check connection
        result = await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")

        # Create all tables
        print("📦 Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ All tables created successfully")

    print("🎉 Database initialization complete!")


async def drop_all_tables():
    """Drop all tables (use with caution!)."""
    print("⚠️  Dropping all tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print("✅ All tables dropped")


async def check_tables():
    """Check which tables exist."""
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]

    print(f"📋 Existing tables ({len(tables)}):")
    for table in tables:
        print(f"   - {table}")

    return tables


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PromptCraft Database Management")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check existing tables"
    )

    args = parser.parse_args()

    if args.check:
        asyncio.run(check_tables())
    else:
        if args.drop:
            confirm = input("Are you sure you want to drop all tables? (yes/no): ")
            if confirm.lower() == "yes":
                asyncio.run(drop_all_tables())
            else:
                print("Cancelled")
                sys.exit(0)

        asyncio.run(init_database())
