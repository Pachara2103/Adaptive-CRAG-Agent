from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import GradeDocument, GradeAnswer
from src.model import gemma, gemini

def get_document_grader_chain():

    system_propmt = """
      You are a document grader. 
      Only Answer binary score 'yes' if the context contains some keyword to the question, 'no' otherwise'. 
      No explanation. If user question is empty, answer 'no'.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_propmt),
            ("human", "Document: {document}\n\nQuestion: {question}"),
        ]
    )

    chain = prompt | gemma.with_structured_output(GradeDocument)

    return chain


def get_answer_grade_chain():

    system_prompt = """
      You are a grader assessing whether an answer addresses the user question.

      Give a binary score 'yes' or 'no'. 
      - 'yes' means the answer is fully supported in the context and addresses the user question.
      - 'no' means the answer is not address the user question.
      """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Question: {question}\n\nContext: {context}\n\nAnswer: {answer}\n\n",  ),
        ]
    )

    chain = prompt | gemini.with_structured_output(GradeAnswer)

    return chain
