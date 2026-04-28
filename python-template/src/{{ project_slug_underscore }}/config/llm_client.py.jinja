"""Claude Agent SDK options factory."""

from claude_agent_sdk import ClaudeAgentOptions

from {{ project_slug_underscore }}.config import get_settings


def build_options(system_prompt: str, tools: list) -> ClaudeAgentOptions:
    s = get_settings()
    if s.llm_provider != "anthropic":
        raise ValueError("Claude Agent SDK template only supports llm_provider=anthropic.")
    return ClaudeAgentOptions(
        model=s.model_id,
        system_prompt=system_prompt,
        max_turns=8,
        allowed_tools=[t.name for t in tools],
    )
