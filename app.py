"""Streamlit UI для AI-агента."""

import streamlit as st
from app.agent import create_agent_instance, ask

st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Agent на LangGraph")
st.caption("ReAct-агент с инструментами: калькулятор, погода, RAG")

# Sidebar
with st.sidebar:
    st.header("⚙️ Настройки")
    use_rag = st.checkbox("Использовать RAG (поиск по документам)", value=False)
    chroma_dir = st.text_input("Папка ChromaDB", value="./chroma_db")
    st.markdown("---")
    st.markdown("**Инструменты:**")
    st.markdown("- 🧮 Калькулятор")
    st.markdown("- 🌤 Погода (OpenWeatherMap)")
    if use_rag:
        st.markdown("- 📚 Поиск по базе знаний")


# Инициализация агента
@st.cache_resource
def get_agent(use_rag, chroma_dir):
    return create_agent_instance(use_rag=use_rag, chroma_dir=chroma_dir)


agent = get_agent(use_rag, chroma_dir)

# История чата
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ввод
if prompt := st.chat_input("Задай вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                response = ask(agent, prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Ошибка: {e}")