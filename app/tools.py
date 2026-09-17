"""Инструменты для AI-агента."""

import math
import requests
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# ============================================================
# 1. Калькулятор
# ============================================================
@tool
def calculator(expression: str) -> str:
    """Вычисляет математическое выражение.
    Пример: '2 + 2 * 3', 'sqrt(16)', 'sin(0)'.
    Поддерживает: +, -, *, /, **, sqrt, sin, cos, tan, log, pi, e.
    """
    try:
        allowed = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round,
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Результат: {result}"
    except Exception as e:
        return f"Ошибка вычисления: {e}"


# ============================================================
# 2. Погода (OpenWeatherMap API — опционально)
# ============================================================
@tool
def weather(city: str) -> str:
    """Возвращает текущую погоду в городе.
    Пример: 'Иркутск', 'Москва'.
    Требует API-ключ OpenWeatherMap в .env (опционально).
    """
    import os
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "API-ключ OpenWeatherMap не настроен. Пропусти этот инструмент."

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "ru"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Погода в {city}: {desc}, {temp}°C"
    except Exception as e:
        return f"Ошибка получения погоды: {e}"


# ============================================================
# 3. RAG — поиск по базе знаний (ChromaDB)
# ============================================================
def create_rag_tool(chroma_dir: str = "./chroma_db"):
    """Создаёт инструмент поиска по векторной БД."""
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434",
    )
    vectorstore = Chroma(
        persist_directory=chroma_dir,
        embedding_function=embeddings,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    @tool
    def search_knowledge_base(query: str) -> str:
        """Ищет информацию в базе знаний (PDF-документы).
        Используй, когда нужен ответ по загруженным документам.
        """
        try:
            docs = retriever.invoke(query)
            if not docs:
                return "В базе знаний нет информации по этому запросу."
            return "\n\n---\n\n".join(doc.page_content for doc in docs)
        except Exception as e:
            return f"Ошибка поиска: {e}"

    return search_knowledge_base


# ============================================================
# Список инструментов
# ============================================================
def get_tools(use_rag: bool = False, chroma_dir: str = "./chroma_db"):
    """Возвращает список инструментов для агента."""
    tools = [calculator, weather]
    if use_rag:
        tools.append(create_rag_tool(chroma_dir))
    return tools