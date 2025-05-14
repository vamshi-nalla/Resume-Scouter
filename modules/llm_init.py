# modules/llm_init.py

from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq

def load_llm(provider: str, model: str, api_key: str):
    if provider == "openai":
        return ChatOpenAI(openai_api_key=api_key, model=model, temperature=0)
    elif provider == "groq":
        return ChatGroq(groq_api_key=api_key, model_name=model, temperature=0)
    else:
        raise ValueError("Unsupported LLM provider. Use 'openai' or 'groq'.")
