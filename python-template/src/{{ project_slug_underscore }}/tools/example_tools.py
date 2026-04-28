"""Claude Agent SDK tools — uses the @tool decorator from claude_agent_sdk."""

import ast
import operator
from typing import Any

from claude_agent_sdk import tool

_MOCK_RESULTS = [
    {"title": "Tokyo - Wikipedia", "url": "https://en.wikipedia.org/wiki/Tokyo",
     "snippet": "Tokyo is the capital of Japan with a population of approximately 13,960,000 (2024)."},
    {"title": "Tokyo Statistics", "url": "https://www.metro.tokyo.lg.jp/english/about/",
     "snippet": "As of 2024, Greater Tokyo has 13.96 million residents."},
    {"title": "World Population Review — Tokyo",
     "url": "https://worldpopulationreview.com/world-cities/tokyo-population",
     "snippet": "Tokyo's 2024 population: 13,960,000."},
]

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
    ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsupported node: {type(node).__name__}")


@tool("web_search", "Search the web (mocked).", {"query": str})
async def web_search(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": str(_MOCK_RESULTS)}]}


@tool("calculator", "Evaluate a safe arithmetic expression.", {"expression": str})
async def calculator(args: dict[str, Any]) -> dict[str, Any]:
    result = _eval(ast.parse(args["expression"], mode="eval").body)
    return {"content": [{"type": "text", "text": str(result)}]}


TOOLS = [web_search, calculator]
