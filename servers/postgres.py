"""PostgreSQL MCP server — query, schema, explain."""
import asyncio, os
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import asyncpg

server = Server("postgres")
DB_URL = os.getenv("DATABASE_URL", "postgresql://localhost/mydb")

@server.list_tools()
async def list_tools():
    return [
        types.Tool(name="query", description="Execute a SQL query (read-only)", inputSchema={"type":"object","properties":{"sql":{"type":"string"}},"required":["sql"]}),
        types.Tool(name="list_tables", description="List all tables in the database", inputSchema={"type":"object","properties":{}}),
        types.Tool(name="describe_table", description="Get table schema", inputSchema={"type":"object","properties":{"table":{"type":"string"}},"required":["table"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    conn = await asyncpg.connect(DB_URL)
    try:
        if name == "query":
            rows = await conn.fetch(arguments["sql"])
            return [types.TextContent(type="text", text=str([dict(r) for r in rows[:50]]))]
        elif name == "list_tables":
            rows = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            return [types.TextContent(type="text", text=str([r["table_name"] for r in rows]))]
        elif name == "describe_table":
            rows = await conn.fetch("SELECT column_name, data_type FROM information_schema.columns WHERE table_name=$1", arguments["table"])
            return [types.TextContent(type="text", text=str([dict(r) for r in rows]))]
    finally:
        await conn.close()
    return [types.TextContent(type="text", text="Unknown tool")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
