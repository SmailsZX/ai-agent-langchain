"""Тесты агента (без вызова LLM)."""

from app.agent import create_agent_instance, ask


def test_agent_creation():
    """Агент создаётся без ошибок."""
    agent = create_agent_instance(use_rag=False)
    assert agent is not None


def test_agent_has_tools():
    """У агента есть инструменты."""
    agent = create_agent_instance(use_rag=False)
    # Проверяем, что агент — это граф LangGraph
    assert hasattr(agent, "invoke")


def test_ask_returns_string():
    """ask() возвращает строку (без реального вызова — мок)."""
    class MockAgent:
        def invoke(self, data):
            return {"messages": [type("Msg", (), {"content": "Ответ"})()]}

    result = ask(MockAgent(), "Тест")
    assert isinstance(result, str)
    assert result == "Ответ"