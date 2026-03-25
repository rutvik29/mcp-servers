# 🔌 MCP Servers

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-1.0-FF6B35?style=flat)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **7 production-ready MCP servers** — connect Claude and any MCP-compatible AI to your real tools: GitHub, Slack, Notion, PostgreSQL, S3, Linear, and web search.

## Included Servers

| Server | Tools Exposed | Transport |
|--------|--------------|-----------|
| `github` | repos, issues, PRs, code search | stdio |
| `slack` | channels, messages, users | stdio |
| `notion` | pages, databases, search | stdio |
| `postgres` | query, schema, tables | stdio |
| `s3` | list, get, put, delete objects | stdio |
| `linear` | issues, projects, cycles | stdio |
| `web-search` | Brave Search API, scrape, summarize | stdio |

## Quick Start

```bash
git clone https://github.com/rutvik29/mcp-servers
cd mcp-servers

# Install all servers
pip install -r requirements.txt

# Add to Claude Desktop config (~/.claude/config.json)
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["-m", "servers.github"],
      "env": {"GITHUB_TOKEN": "ghp_..."}
    },
    "postgres": {
      "command": "python",
      "args": ["-m", "servers.postgres"],
      "env": {"DATABASE_URL": "postgresql://..."}
    }
  }
}
```

## License
MIT © Rutvik Trivedi
