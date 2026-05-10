import asyncio
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

client = Anthropic()

async def run_turn(session, tools, messages):
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\nAgent: {block.text}")
            messages.append({"role": "assistant", "content": response.content})
            return

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"Calling tool: {block.name} with {block.input}")
                result = await session.call_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result.content[0].text
                })

        messages.append({"role": "user", "content": tool_results})


async def chat():
    server_params = StdioServerParameters(
        command="./venv/bin/python",
        args=["server.py"],
        env={"GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN")}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools_result.tools
            ]

            print(f"Available tools: {[t['name'] for t in tools]}")
            print("Type a goal and press enter. Type 'exit' or Ctrl-D to quit.\n")

            messages = []

            while True:
                try:
                    goal = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break

                if not goal:
                    continue
                if goal.lower() in {"exit", "quit"}:
                    break

                messages.append({"role": "user", "content": goal})
                try:
                    await run_turn(session, tools, messages)
                except KeyboardInterrupt:
                    print("\n(interrupted)")
                    break

            print("Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nGoodbye!")
