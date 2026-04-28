"""Claude Agent SDK tool tests. Decorated tools are async and return content envelopes."""

import asyncio

from {{ project_slug_underscore }}.tools.example_tools import calculator, web_search


def test_web_search_returns_mock_envelope() -> None:
    out = asyncio.run(web_search.handler({"query": "Tokyo"}))
    assert "content" in out and out["content"][0]["type"] == "text"


def test_calculator_basic_arithmetic() -> None:
    out = asyncio.run(calculator.handler({"expression": "13960000 / 1000"}))
    assert out["content"][0]["text"] == "13960.0"


def test_calculator_rejects_unsafe_expression() -> None:
    import pytest
    with pytest.raises(Exception):
        asyncio.run(calculator.handler({"expression": "__import__('os').system('echo pwned')"}))
