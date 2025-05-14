from pydantic import BaseModel, Field
from typing import List, Dict

class RepoSummary(BaseModel):
    summary: str
    skills_used: Dict = Field(default_factory=dict)

class ResumeAnalysis(BaseModel):
    name: str
    phone_number: str = ""
    gmail_email: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    technical_skills: Dict = Field(default_factory=dict)
    experience: Dict = Field(default_factory=dict)
    projects: Dict = Field(default_factory=dict)
    education: Dict = Field(default_factory=dict)
    certifications: Dict = Field(default_factory=dict)
    algorithms: List[str] = Field(default_factory=list)
    statistics_concepts: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)

class FullAnalysis(BaseModel):
    resume_analysis: ResumeAnalysis
    github_analysis: List[RepoSummary]
