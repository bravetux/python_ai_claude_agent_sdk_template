# Python AI Claude Agent SDK Template (`python_ai_claude_agent_sdk_template`)

A Copier template for bootstrapping production-ready AI agent projects using the [Claude Agent SDK](https://docs.claude.com/en/docs/claude-code/agent-sdk) (Anthropic), with a Streamlit chat UI and a modern Python toolchain: `uv`, `ruff`, tests, docs, Docker, and releases.

## Why this template
- Start fast with the **same agent loop that powers Claude Code** — `ClaudeSDKClient` + in-process MCP tool server.
- Includes working examples of `@tool` decorated async functions, `create_sdk_mcp_server`, and `ClaudeAgentOptions`.
- Streamlit chat UI with session management ready to go.
- Keep quality automated with linting, formatting, type checking, and tests.

## ⚠️ Provider caveat — Anthropic only

The Claude Agent SDK is purpose-built for Anthropic Claude models. This template **only supports `LLM_PROVIDER=anthropic`** — the `llm_client.py` raises a `ValueError` if you set `bedrock` or `openai`. If you need cross-provider, use the `python_ai_langgraph_template` or `python_ai_pydanticai_template` instead.

## Technology stack
- [Claude Agent SDK](https://docs.claude.com/en/docs/claude-code/agent-sdk) — the Python SDK that powers Claude Code's agent loop.
- [Streamlit](https://streamlit.io/) for the web chat UI.
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for typed configuration.
- [Copier](https://copier.readthedocs.io/), [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), `pre-commit`, `pytest`, [MkDocs](https://www.mkdocs.org/) Material, [Docker](https://www.docker.com/).
- `AGENTS.md.jinja` to generate a project-specific `AGENTS.md`.

## Usage

```bash
uvx copier copy Template/python_ai_claude_agent_sdk_template my_first_agent \
  --data package_name=my_first_agent \
  --data project_description="My first agent" \
  --data github_username=YOU
```

## Quick start

### 1. Install [`uv`](https://github.com/astral-sh/uv)

### 2. Create the project using copier

```bash
uvx copier copy <path-to>/python_ai_claude_agent_sdk_template my-claude-agent
```

| Prompt | Description |
|--------|-------------|
| `package_name` | Name of the Python AI agent package |
| `project_description` | Short description of the project |
| `github_username` | GitHub username or organization name |

### 3. Setup

```bash
cd my-claude-agent
git init --initial-branch=main
cp .env.example .env
# Edit .env — ANTHROPIC_API_KEY required
make install
git add . && git commit -m "feat: first commit"
```

### 4. Run the agent

```bash
make run     # CLI single query
make repl    # CLI interactive REPL
make ui      # Streamlit UI
```

## Generated project structure

```
your-project/
├── app.py
├── main.py
├── pyproject.toml
├── Makefile
├── .env.example
├── AGENTS.md
├── src/<package>/
│   ├── config/
│   │   ├── settings.py                 # pydantic-settings (anthropic-only)
│   │   ├── llm_client.py               # ClaudeAgentOptions factory
│   │   └── prompts.py
│   ├── agents/
│   │   ├── orchestrator.py             # ClaudeSDKClient with in-process MCP server
│   │   └── example_agent.py            # create_sdk_mcp_server(name, version, tools)
│   ├── tools/
│   │   └── example_tools.py            # @tool("name", "desc", schema) async functions
│   └── ui/
│       └── components.py
├── tests/
│   ├── conftest.py
│   ├── test_example_tools.py           # asyncio.run + tool.handler({...}) tests
│   └── test_settings.py
├── docker/
├── docs/
├── scripts/
└── playground/notebook.py
```

## Architecture

```
User Query
    │
    ▼ asyncio.run
┌────────────────────────────┐
│   ClaudeSDKClient           │  ← agent loop (Claude Code's loop, in your process)
└────────────┬───────────────┘
             │ tool calls via in-process MCP
             ▼
┌────────────────────────────┐
│   create_sdk_mcp_server     │  ← name="researcher_tools", tools=[web_search, calculator]
└──┬──────────────────────┬──┘
   │                      │
   ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ web_search   │    │ calculator   │   ← @tool decorated async functions
└──────────────┘    └──────────────┘
```

### Key patterns

- **`ClaudeSDKClient`** — runs the agent loop. Use as an async context manager.
- **In-process MCP server** — `create_sdk_mcp_server(name, version, tools)` registers your tools as if they were on a remote MCP server, but inside your process.
- **`@tool` decorator** — from `claude_agent_sdk`. Signature is `@tool(name, description, input_schema)` where `input_schema` is `{"param": type}`. The decorated function is async and returns `{"content": [{"type": "text", "text": "..."}]}`.
- **`ClaudeAgentOptions`** — system prompt, allowed tool names, max turns, MCP servers map.
- **Receiving the response** — `async for msg in client.receive_response(): ...` — collect messages where `hasattr(msg, "result")`.
- **Configuration** — `pydantic-settings` loads from `.env`. Provider is locked to `anthropic`.

## Adding a new tool

1. **Create tool** in `src/<package>/tools/my_tools.py`:

   ```python
   from claude_agent_sdk import tool

   @tool("fetch_data", "Fetch data for the given query.", {"query": str})
   async def fetch_data(args: dict) -> dict:
       result = {"result": "..."}
       return {"content": [{"type": "text", "text": str(result)}]}
   ```

2. **Add to TOOLS** — append to the `TOOLS` list in `tools/example_tools.py` (or create your own list and import it):

   ```python
   from <package>.tools.my_tools import fetch_data

   TOOLS = [web_search, calculator, fetch_data]
   ```

3. **Update `allowed_tools`** — `ClaudeAgentOptions` reads `[t.name for t in tools]` automatically in this template; no extra wiring needed.

4. **Write tests** in `tests/test_my_tools.py`:

   ```python
   import asyncio
   from <package>.tools.my_tools import fetch_data

   def test_fetch():
       out = asyncio.run(fetch_data.handler({"query": "foo"}))
       assert "content" in out
   ```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `anthropic` | **Must remain `anthropic`** for this template |
| `ANTHROPIC_API_KEY` | | **Required** |
| `MODEL_ID` | `claude-sonnet-4-6` | Anthropic model ID |
| `MAX_TOKENS` | `2048` | Max response tokens |
| `TEMPERATURE` | `0.7` | LLM temperature |
| `LOG_LEVEL` | `INFO` | Logging level |

`AWS_*`, `BEDROCK_*`, and `OPENAI_*` env vars are present in `.env.example` (consistency with sibling templates) but are not used.

## Makefile commands

| Command | Description |
|---------|-------------|
| `make install` | Installs dependencies and pre-commit hooks |
| `make run` | CLI: runs the default query |
| `make repl` | CLI: REPL |
| `make ui` | Streamlit UI |
| `make test` | pytest |
| `make lint` | Ruff |
| `make typecheck` | `ty` |
| `make format` | Ruff format |
| `make docs` | MkDocs serve |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run container |
| `make clean` | Clean caches |

## Documentation

```bash
make docs
```

## Update an existing project

```bash
uvx copier update --defaults
```
