from langchain_core.messages import ToolMessage

from src.utils.vector_store import vector_store
from state import AgentState
from chains.rewriter import get_rewriter_chain
from chains.grader import get_answer_grade_chain, get_document_grader_chain
from chains.agent import get_agent_chain



def rewrite_query_node(state: AgentState) -> AgentState:
    print("--- Call Rewriter ---\n")
    question = state["question"]

    rewrite_chain = get_rewriter_chain()
    better_question = rewrite_chain.invoke({"question": question})
    print(f"\n{better_question.content}\n")

    return {"question": better_question.content}


def retrieve_documents_node(state: AgentState) -> AgentState:
    """Use this tool to search for relevant documents in database based on the user input."""
    print("--- Call Retriever ---\n")

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    documents = retriever.invoke(state["question"])
    print(f'\n{documents}\n')

    return {"documents": documents}


def grade_document_node(state: AgentState) -> AgentState:
    print("--- Call Document Grader ---\n")
    docs = state["documents"]
    filtered_content = []
    
    document_grader_chain = get_document_grader_chain()
    for doc in docs:
        res = document_grader_chain.invoke({"document": doc.page_content, "question": state["question"]})
        if res.binary_score == "yes":
            filtered_content.append(doc.page_content)
            
    return {"filtered_documents": filtered_content}


def agent_node(state: AgentState) -> AgentState:
    print("--- Call Agent ---\n")

    context = "\n\n".join(state["filtered_documents"]) #problem ถ้า tool calls ให้ใช้ from web 

    agent_chain = get_agent_chain()
    response = agent_chain.invoke({"context": context, "messages": state["messages"]})

    last_message = state["messages"][-1]

    if isinstance(last_message, ToolMessage):
        context = last_message.content

    return {"messages": [response], "context": context}


def grade_answer_node(state: AgentState) -> AgentState:
    print("--- Call Answer Grader ---\n")
    
    question = state["question"]
    context = state["context"]
    answer = state["messages"][-1].content
    
    print(f'question: {question}\n context: {context}\n answer: {answer}\n\n')
    
    if isinstance(answer , list):
            answer  = "".join([item.get('text', '') for item in answer if item.get('type') == 'text'])
        
    answer_grader_chain = get_answer_grade_chain()
    score = answer_grader_chain.invoke({"question": question, "context": context, "answer": answer})
    
    grade = score.binary_score
    print(f"--- ANSWER GRADE: {grade} ---\n")
    
    return {"grade": grade} 
