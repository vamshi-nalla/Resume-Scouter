import streamlit as st
import os
import tempfile
from modules.prompts import load_prompts
from modules.llm_init import initialize_llm
from modules.parser import build_resume_chain, build_repo_chain
from modules.analyzer import analyze_resume

st.set_page_config(page_title="Resume + GitHub Analyzer", layout="centered")
st.title("📄 AI-Powered Resume + GitHub Analyzer")

# API keys and model selection
with st.expander("🔐 Enter API Credentials"):
    openai_key = st.text_input("OpenAI API Key", type="password")
    openai_model = st.selectbox("OpenAI Model", ["gpt-4", "gpt-3.5-turbo", "o3-mini"])
    groq_key = st.text_input("Groq API Key", type="password")
    groq_model = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama3-8b-8192"])
    github_token = st.text_input("GitHub Access Token", type="password")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF only)", type=["pdf"])

if st.button("🚀 Analyze") and uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    prompts = load_prompts()
    provider = "openai" if openai_key else "groq"
    llm = initialize_llm(openai_key or groq_key, provider, openai_model if openai_key else groq_model)
    
    resume_chain = build_resume_chain(llm, prompts)
    repo_chain = build_repo_chain(llm, prompts)

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    out_file, full_analysis = analyze_resume(tmp_path, resume_chain, repo_chain, github_token, output_dir)
    
    st.success("✅ Analysis complete!")
    st.json(full_analysis.dict())
    
    with open(out_file, "rb") as f:
        st.download_button("📥 Download Analysis JSON", f, file_name=os.path.basename(out_file), mime="application/json")

    # Corporate Summary
    st.subheader("📊 Corporate Resume Summary")
    summary = full_analysis.resume_analysis
    st.markdown(f"""
    **Name:** {summary.name}  
    **Email:** {summary.gmail_email}  
    **Phone:** {summary.phone_number}  
    **LinkedIn:** {summary.linkedin_url}  
    **GitHub:** {summary.github_url}  
    
    ### Skills
    - {", ".join(summary.technical_skills.keys())}
    
    ### Experience
    - {", ".join(summary.experience.keys())}
    
    ### Projects
    - {", ".join(summary.projects.keys())}
    """)

