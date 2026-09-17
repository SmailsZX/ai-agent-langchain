"""Тесты инструментов агента."""

from app.tools import calculator, get_tools


def test_calculator_simple():
    """Простое выражение."""
    result = calculator.invoke("2 + 2")
    assert "4" in result


def test_calculator_priority():
    """Приоритет операций."""
    result = calculator.invoke("2 + 2 * 3")
    assert "8" in result


def test_calculator_sqrt():
    """Квадратный корень."""
    result = calculator.invoke("sqrt(16)")
    assert "4" in result


def test_calculator_error():
    """Ошибка — невалидное выражение."""
    result = calculator.invoke("2 + ")
    assert "Ошибка" in result


def test_get_tools_without_rag():
    """Без RAG — 2 инструмента."""
    tools = get_tools(use_rag=False)
    assert len(tools) == 2
    names = [t.name for t in tools]
    assert "calculator" in names
    assert "weather" in names


def test_get_tools_with_rag():
    """С RAG — 3 инструмента."""
    tools = get_tools(use_rag=True, chroma_dir="./chroma_db")
    assert len(tools) == 3
    names = [t.name for t in tools]
    assert "search_knowledge_base" in names