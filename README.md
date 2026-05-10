# JM Portfolio MCP

A two-part Python project demonstrating end-to-end MCP (Model Context Protocol) development: a server that exposes GitHub data as tools, and an interactive agent that uses those tools to let you chat with your repositories in natural language.

Built as a portfolio project to demonstrate hands-on MCP development with the Anthropic Claude ecosystem.

## Components

### `server.py` — MCP Server

A FastMCP server that exposes three GitHub tools to any MCP-compatible client:

- **list_repos** — List public repositories for any GitHub user
- **get_repo** — Get detailed information about a specific repository
- **list_repo_contents** — Browse files and directories within a repository

### `agent.py` — Interactive CLI Agent

A chat loop that connects to `server.py` over stdio, hands the tools to Claude, and lets you ask questions in plain English. Conversation history is preserved across turns, so follow-up questions ("now show me its contents") work without restating context. Tool calls are printed as they happen, so you can see exactly what the agent is doing.

## Tech Stack

- Python
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [PyGithub](https://github.com/PyGithub/PyGithub)

## Setup

1. Clone the repo and `cd` into it.

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   ./venv/bin/pip install mcp pygithub anthropic python-dotenv
   ```

4. Create a `.env` file in the project root with both credentials:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

   - The GitHub token needs `repo` read scope. Generate one at https://github.com/settings/tokens.
   - Get an Anthropic API key from https://console.anthropic.com.

## Usage

### Inspector mode — exercise the server's tools directly

```bash
./venv/bin/mcp dev server.py
```

This launches the MCP Inspector in your browser, where you can call each tool interactively and inspect inputs/outputs. Useful for verifying the server in isolation.

### Chat mode — talk to your repos through the agent

```bash
./venv/bin/python agent.py
```

This starts the interactive CLI. The agent spawns `server.py` as a subprocess, lists its tools, and waits for input.

```
Available tools: ['list_repos', 'get_repo', 'list_repo_contents']
Type a goal and press enter. Type 'exit' or Ctrl-D to quit.

You: list 4pt1y's repos and tell me which one looks most active
Calling tool: list_repos with {'username': '4pt1y'}

Agent: ...
```

Exit with `exit`, `quit`, Ctrl-D, or Ctrl-C.

## Why MCP?

MCP is a standardized protocol that connects AI agents to external tools and data sources — think of it as the USB standard for AI integrations. By exposing GitHub data through MCP, the same server can be consumed by `agent.py`, the MCP Inspector, Claude Desktop, or any other MCP-compatible client without custom integration work.

## Author

John Miller — [GitHub](https://github.com/4pt1y)
