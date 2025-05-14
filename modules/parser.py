from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from modules.models import ResumeAnalysis, RepoSummary, FullAnalysis

def get_resume_chain(prompt_data: dict, llm):
    resume_parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
    resume_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system"]),
        ("human", prompt_data["human"])
    ])
    resume_prompt = resume_prompt.partial(format_instructions=resume_parser.get_format_instructions())
    return resume_prompt | llm | resume_parser

def get_repo_chain(prompt_data: dict, llm):
    repo_parser = PydanticOutputParser(pydantic_object=RepoSummary)
    repo_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system"]),
        ("human", prompt_data["human"])
    ])
    repo_prompt = repo_prompt.partial(format_instructions=repo_parser.get_format_instructions())
    return repo_prompt | llm | repo_parser

def summarize_analysis(analysis: FullAnalysis, prompt_data: dict, llm):
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system"]),
        ("human", prompt_data["human"])
    ])
    summary_chain = summary_prompt | llm | StrOutputParser()
    return summary_chain.stream({"data": analysis.json()})
