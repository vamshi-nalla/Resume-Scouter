import os
import tempfile
from modules.utils import (
    extract_text_and_links,
    extract_github_username,
    fetch_repos,
    fetch_readme,
    fetch_languages
)
from modules.models import FullAnalysis, RepoSummary
from modules.parser import get_resume_chain, get_repo_chain
from langchain_core.language_models.chat_models import BaseChatModel


def analyze_resume_and_github(uploaded_file, prompts: dict, llm: BaseChatModel, github_token: str) -> FullAnalysis:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Extract text and links from resume
    text, links = extract_text_and_links(tmp_path)
    os.remove(tmp_path)  # Clean up

    # Initialize LangChain pipelines
    resume_chain = get_resume_chain(prompts["resume"], llm)
    repo_chain = get_repo_chain(prompts["github"], llm)

    # Run resume analysis
    resume_result = resume_chain.invoke({"text": text, "links": str(links)})

    # Extract GitHub username from resume and analyze repos
    username = extract_github_username(resume_result.github_url)
    github_results = []

    if username:
        for repo in fetch_repos(username, github_token):
            try:
                readme = fetch_readme(username, repo["name"], github_token)
                langs = fetch_languages(username, repo["name"], github_token)
                result: RepoSummary = repo_chain.invoke({
                    "name": repo["name"],
                    "description": repo.get("description", ""),
                    "languages": langs,
                    "readme": readme[:10000]  # truncate to avoid model overload
                })
                github_results.append(result)
            except Exception as e:
                print(f"GitHub repo analysis error ({repo['name']}): {e}")

    return FullAnalysis(resume_analysis=resume_result, github_analysis=github_results)
