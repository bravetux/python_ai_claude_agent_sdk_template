"""Claude Agent SDK orchestrator — uses ClaudeSDKClient over the in-process MCP server."""

import asyncio
from typing import Callable

from claude_agent_sdk import ClaudeSDKClient

from {{ project_slug_underscore }}.agents.example_agent import build_researcher_server
from {{ project_slug_underscore }}.config.llm_client import build_options
from {{ project_slug_underscore }}.config.prompts import RESEARCHER_PROMPT
from {{ project_slug_underscore }}.tools.example_tools import TOOLS


def build_orchestrator() -> Callable[[str], str]:
    server = build_researcher_server()
    options = build_options(system_prompt=RESEARCHER_PROMPT, tools=TOOLS)
    options.mcp_servers = {"researcher": server}

    async def _run_async(query: str) -> str:
        async with ClaudeSDKClient(options=options) as client:
            await client.query(query)
            chunks: list[str] = []
            async for msg in client.receive_response():
                if hasattr(msg, "result"):
                    chunks.append(str(msg.result))
            return "".join(chunks)

    def run(query: str) -> str:
        return asyncio.run(_run_async(query))

    return run
