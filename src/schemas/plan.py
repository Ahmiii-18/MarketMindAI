from typing import List
from pydantic import BaseModel, Field

class SubQuestion(BaseModel):
    id: str = Field(description="Unique identifier for the sub-question")
    question_text: str = Field(description="The specific sub-question to research")

class Objective(BaseModel):
    id: str = Field(description="Unique identifier for the strategic objective")
    title: str = Field(description="Title of the strategic objective")
    sub_questions: List[SubQuestion] = Field(default_factory=list)

class ResearchPlan(BaseModel):
    research_objective: str = Field(description="Core objective of the research")
    assumptions: List[str] = Field(default_factory=list)
    objectives: List[Objective] = Field(default_factory=list)