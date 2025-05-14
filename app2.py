import streamlit as st
from modules.llm_init import load_llm
from modules.prompts import load_prompts
from modules.analyzer import analyze_resume_and_github
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json


st.set_page_config(page_title="Resume & GitHub Analyzer", layout="wide")

st.title("🤖 Resume + GitHub Analyzer")
st.markdown("Upload your resume, enter your API keys, and get structured insights and an executive summary.")

# --- Sidebar API Keys and Model Selection ---
with st.sidebar:
    st.header("🔐 API Configuration")

    openai_key = st.text_input("OpenAI API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    github_token = st.text_input("GitHub Access Token", type="password")

    st.markdown("### 🔧 Model Selection")

    selected_llm = None
    model_choice = None

    if openai_key:
        model_choice = st.selectbox("OpenAI Model", ["gpt-4", "gpt-3.5-turbo"])
        selected_llm = load_llm(provider="openai", model=model_choice, api_key=openai_key)
    elif groq_key:
        model_choice = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama3-8b-8192"])
        selected_llm = load_llm(provider="groq", model=model_choice, api_key=groq_key)
    else:
        st.warning("Please provide either OpenAI or Groq API key.")

# --- Resume Upload Section ---
uploaded_file = st.file_uploader("📄 Upload a PDF Resume", type=["pdf"])

if uploaded_file and selected_llm and github_token:
    with st.spinner("Analyzing... Please wait"):
        prompts = load_prompts()
        full_analysis = analyze_resume_and_github(uploaded_file, prompts, selected_llm, github_token)

        # Display structured JSON output
        st.subheader("📊 Structured Analysis")
        st.json(full_analysis.dict())

        # Generate executive summary using LLM
        def generate_summary(llm, analysis_dict):
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a professional HR analyst writing corporate-level summaries."),
                ("human", "Summarize the following resume and GitHub analysis into an executive summary:\n\n{input}")
            ])
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"input": json.dumps(analysis_dict)})

        st.subheader("📝 Executive Summary")

        summary_text = generate_summary(selected_llm, full_analysis.dict())

        for section in summary_text.split("\n\n"):
            if ":" in section:
                title, body = section.split(":", 1)
                st.markdown(f"**{title.strip()}:** {body.strip()}")
            else:
                st.markdown(section.strip())

elif not uploaded_file:
    st.info("Please upload a PDF resume to get started.")
elif not github_token:
    st.warning("GitHub Access Token is required for GitHub repo analysis.")
elif not selected_llm:
    st.warning("Please select a valid API key and model.")
