"""ReAct-агент на LangChain 1.x (create_agent)."""

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.tools import get_tools


def create_agent_instance(use_rag: bool = False, chroma_dir: str = "./chroma_db"):
    """Создаёт ReAct-агента с инструментами."""
    llm = ChatOllama(
        model="qwen2.5:7b-instruct-q4_K_M",
        base_url="http://localhost:11434",
        temperature=0.1,
    )

    tools = get_tools(use_rag=use_rag, chroma_dir=chroma_dir)

    system_prompt = """Ты — полезный AI-ассистент с инструментами.

Правила:
1. Если нужен расчёт — используй calculator.
2. Если нужна погода — используй weather.
3. Если вопрос по документам — используй search_knowledge_base.
4. Если инструмент не нужен — отвечай напрямую.
5. Отвечай кратко и по делу, на русском языке.
6. Не выдумывай факты. Если не знаешь — скажи об этом.
"""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent


def ask(agent, question: str) -> str:
    """Задаёт вопрос агенту, возвращает ответ."""
    result = agent.invoke({"messages": [("user", question)]})
    return result["messages"][-1].content