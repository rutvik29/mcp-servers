"""GitHub MCP server — repos, issues, PRs, code search."""
import asyncio, os
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import httpx

GH_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
BASE = "https://api.github.com"

server = Server("github")

@server.list_tools()
async def list_tools():
    return [
        types.Tool(name="search_repos", description="Search GitHub repositories", inputSchema={"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}),
        types.Tool(name="list_issues", description="List issues for a repo", inputSchema={"type":"object","properties":{"repo":{"type":"string"},"state":{"type":"string","default":"open"}},"required":["repo"]}),
        types.Tool(name="create_issue", description="Create a GitHub issue", inputSchema={"type":"object","properties":{"repo":{"type":"string"},"title":{"type":"string"},"body":{"type":"string"}},"required":["repo","title"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        if name == "search_repos":
            r = await client.get(f"{BASE}/search/repositories", params={"q": arguments["query"], "per_page": 10})
            items = r.json().get("items", [])
            return [types.TextContent(type="text", text=str([{"name": i["full_name"], "stars": i["stargazers_count"], "desc": i["description"]} for i in items]))]
        elif name == "list_issues":
            r = await client.get(f"{BASE}/repos/{arguments['repo']}/issues", params={"state": arguments.get("state","open")})
            return [types.TextContent(type="text", text=str([{"number": i["number"], "title": i["title"], "state": i["state"]} for i in r.json()]))]
        elif name == "create_issue":
            r = await client.post(f"{BASE}/repos/{arguments['repo']}/issues", json={"title": arguments["title"], "body": arguments.get("body","")})
            return [types.TextContent(type="text", text=f"Created issue #{r.json().get('number')}: {r.json().get('html_url')}")]
    return [types.TextContent(type="text", text="Unknown tool")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
