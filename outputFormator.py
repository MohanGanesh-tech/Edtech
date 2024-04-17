from pydantic import BaseModel, Field
from enums import KnowledgeLevel, QuestionLevel

class QuestionOutputFormator(BaseModel):
    subject: str = Field(description="The subject of the question")
    question: str = Field(description="The quiz question text")
    options: list = Field(description="A list of options for the multiple-choice question, if it is MCQ then give Options else []")
    current_question_level: QuestionLevel = Field(description="The difficulty level of the question")

class EachAnswerEvaluatorOutputFormator(BaseModel):
    review: str = Field(description="Review of the answer")
    feedback: str = Field(description="Feedback of the answer")
    student_knowledge_level: KnowledgeLevel = Field(description="Based on answer correctness")

class OverallEvaluatorOutputFormator(BaseModel):
    total_number_of_question: int = Field(description="Total number of question asked by AI")
    total_number_of_correct_answer: int = Field(description="Total number of correct answer by Human")
    review_on_each_subject: dict = Field(description="Review on each subject, if Q&A not have converstion about particular subject then review='N/A' else give overall review about student understanding example1:student is good with subject, example2: student want to study more, example3: student should have scope of learning, etc")
    overall_student_knowledge_level: KnowledgeLevel = Field(description="Overall student knowledge level")
