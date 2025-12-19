from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from state import AgentState
from tools import search

from nodes import retrieve_documents_node, rewrite_query_node, grade_answer_node,agent_node, grade_document_node
from edges import should_continue, should_regenerate
def get_workflow():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("rewrite", rewrite_query_node)
    graph.add_node("retriever", retrieve_documents_node)
    graph.add_node("document_grader", grade_document_node)
    graph.add_node("agent", agent_node)
    graph.add_node("answer_grader", grade_answer_node)
    graph.add_node("tools", ToolNode(tools=[search]))

    # Flow
    graph.add_edge(START, "rewrite")
    graph.add_edge("rewrite", "retriever")
    graph.add_edge("retriever", "document_grader")
    graph.add_edge("document_grader", "agent")

    # Conditional flows
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": "answer_grader",
        },
    )

    graph.add_conditional_edges(
        "answer_grader",
        should_regenerate,
        {
            "regenerate": "agent",
            "answer": END,
        },
    )

    graph.add_edge("tools", "agent")

    return graph.compile()
