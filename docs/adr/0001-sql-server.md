# ADR 0001: Use SQL Server 2022 for Development

## Status
Accepted

## Context
ShopLite is a modular monolith with a FastAPI backend, SQLAlchemy 2.x ORM, Alembic migrations, and a React frontend. The technical design records SQL Server 2022 as the primary database for local use, with SQLAlchemy and `pyodbc` used for connectivity. For this training application, the database choice needs to suit a Microsoft-centric workshop environment where participants are likely to be familiar with Microsoft tooling and SQL Server administration.

## Decision
Use SQL Server 2022 for development. This choice is primarily for convenience for participants working in a Microsoft-shop environment, where SQL Server, T-SQL, and related tools are already familiar.

## Consequences
Pros:
- Participants who already work with Microsoft data platforms can use familiar T-SQL concepts and tooling.
- The choice fits well with mature Microsoft ecosystem tools such as SQL Server Management Studio, Azure Data Studio, and ODBC-based integrations.
- Running the same database family in development as the one described in the technical design reduces translation work during the workshop.

Cons:
- ARM-based development machines may need the SQL Server Edge variant rather than the standard SQL Server 2022 container image.
- Local setup requires the ODBC Driver for SQL Server in addition to Python package dependencies.
- SQL Server is heavier than SQLite for fast local unit-test workflows and simple throwaway environments.