# JM Portfolio MCP Server

A Python MCP (Model Context Protocol) server that exposes GitHub repository data as tools for AI agents.

Built as a portfolio project to demonstrate hands-on MCP development using the Anthropic Claude ecosystem.

## What it does

Exposes three tools that any MCP-compatible AI agent can call:

- **list_repos** — List public repositories for any GitHub user
- **get_repo** — Get detailed information about a specific repository
- **list_repo_contents** — Browse files and directories within a repository

## Tech Stack

- Python
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- GitHub API v3

## Setup

1. Clone the repo
2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   ./venv/bin/pip install mcp pygithub
```
4. Generate a GitHub personal access token with `repo` read scope

## Running the server

```bash
export GITHUB_TOKEN=your_token_here
./venv/bin/mcp dev server.py
```

This launches the MCP Inspector in your browser where you can call tools interactively.

## Why MCP?

MCP (Model Context Protocol) is a standardized protocol that connects AI agents to external tools and data sources. Think of it as the USB standard for AI integrations. This server exposes GitHub data in a way that any MCP-compatible agent can consume without custom integration work.

## Author

John Miller — [GitHub](https://github.com/4pt1y)
