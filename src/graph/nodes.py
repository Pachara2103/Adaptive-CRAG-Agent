from langchain_core.messages import ToolMessage
from langchain_core.documents import Document

from src.utils.vector_store import vector_store
from src.graph.state import AgentState
from src.chains.rewriter import get_rewriter_chain
from src.chains.grader import get_answer_grade_chain, get_document_grader_chain
from src.chains.agent import get_agent_chain


def rewrite_query_node(state: AgentState) -> AgentState:
    print("--- Call Rewriter ---\n")
    
    question = state['messages'][-1].content

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
    print(f"\n{documents}\n")

    return {"documents": documents}


def grade_document_node(state: AgentState) -> AgentState:
    print("--- Call Document Grader ---\n")
    docs = state["documents"]
    filtered_content = []

    document_grader_chain = get_document_grader_chain()
    for doc in docs:
        res = document_grader_chain.invoke(
            {"document": doc.page_content, "question": state["question"]}
        )
        print(f"{res.binary_score} {doc.page_content}\n")
        if res.binary_score == "yes":
            filtered_content.append(doc.page_content)

    return {"filtered_documents": filtered_content}


def agent_node(state: AgentState) -> AgentState:
    print("--- Call Agent ---\n")
    last_message = state["messages"][-1]
    agent_chain = get_agent_chain()
    
    if isinstance(last_message, ToolMessage):
        web_documents = []
        raw_results = last_message.artifact
        context=''
        if raw_results:
          for item in raw_results:
            context += f'{item["content"]}\n\n'
            doc = Document(page_content=item["content"], metadata={"source": item["url"]})
            web_documents.append(doc)
            
        response = agent_chain.invoke({"context": context, "messages": state["messages"]})
        
        return {"messages": [response], "context": context, 'filtered_documents':web_documents}

    else:
        context = "\n\n".join([doc for doc in state["filtered_documents"]])
        response = agent_chain.invoke({"context": context, "messages": state["messages"]})
        
        return {"messages": [response], "context": context}


def grade_answer_node(state: AgentState) -> AgentState:
    print("--- Call Answer Grader ---\n")

    question = state["question"]
    context = state["context"]
    answer = state["messages"][-1].content

    print(f"question: {question}\n context: {context}\n answer: {answer}\n\n")

    if isinstance(answer, list):
        answer = "".join(
            [item.get("text", "") for item in answer if item.get("type") == "text"]
        )

    answer_grader_chain = get_answer_grade_chain()
    score = answer_grader_chain.invoke(
        {"question": question, "context": context, "answer": answer}
    )

    grade = score.binary_score
    print(f"--- ANSWER GRADE: {grade} ---\n")

    return {"grade": grade}
