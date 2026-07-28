import os
from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from agent.tools import get_retriever, validate_labs
from agent.prompts import ROUTER_PROMPT, SYNTHESIS_PROMPT

load_dotenv()

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY, temperature=0.3)


def safe_llm_call(prompt):
    """
    Wraps every LLM call with production-grade error handling.
    Distinguishes rate-limit and auth errors from generic failures so the
    user (or site owner) gets an actionable message instead of a vague one.
    """
    try:
        return llm.invoke(prompt).content
    except Exception as e:
        error_text = str(e).lower()
        if "rate limit" in error_text or "429" in error_text:
            return "[Error: The AI model is receiving too many requests right now (free-tier rate limit). Please wait about 30 seconds and try again.]"
        if "api key" in error_text or "unauthorized" in error_text or "401" in error_text:
            return "[Error: The AI service could not authenticate. This is a configuration issue, not something you can fix here — please let the site owner know.]"
        return f"[Error contacting the AI model: {e}. Please try again in a moment.]"


class AgentState(TypedDict):
    question: str
    lab_values: Dict[str, float]
    needs_search: bool
    needs_validation: bool
    retrieved_chunks: List[str]
    lab_results: List[dict]
    final_answer: str
    steps_log: List[str]


def classify_intent(state: AgentState):
    prompt = ROUTER_PROMPT.format(question=state["question"])
    response = safe_llm_call(prompt)
    response_lower = response.lower()

    # Safe default: only skip guideline search if the router EXPLICITLY said
    # "search: false". If the response is malformed or the call failed, we
    # search anyway rather than silently answering with no context.
    needs_search = "search: false" not in response_lower

    needs_validation = "validate: true" in response_lower or bool(state.get("lab_values"))

    log = state.get("steps_log", []) + ["🧭 Classifying question..."]
    return {**state, "needs_search": needs_search, "needs_validation": needs_validation, "steps_log": log}


def check_labs(state: AgentState):
    lab_values = state.get("lab_values") or {}
    log = state["steps_log"] + ["🧪 Checking lab values against reference ranges..."]
    if not lab_values:
        return {**state, "lab_results": [], "steps_log": log}
    try:
        results = validate_labs(lab_values)
    except Exception as e:
        results = [{
            "test_name": "N/A", "value": None, "status": "unknown_test",
            "message": f"Lab validation is temporarily unavailable ({e})."
        }]
    return {**state, "lab_results": results, "steps_log": log}


def synthesize_answer(state: AgentState):
    context = "\n\n".join(state.get("retrieved_chunks", [])) or "No guideline search was needed."
    lab_text = "\n".join([r["message"] for r in state.get("lab_results", [])]) or "No lab values were submitted."
    prompt = SYNTHESIS_PROMPT.format(question=state["question"], context=context, lab_results=lab_text)
    response = safe_llm_call(prompt)
    log = state["steps_log"] + ["✍️ Synthesizing answer..."]
    return {**state, "final_answer": response, "steps_log": log}


def build_graph():
    # Retriever (and its Chroma connection) is created ONCE here, when the
    # agent is built -- not on every question (fixes the Day 6 Chroma bug).
    # If it fails to load (e.g. missing chroma_store/), we don't crash the
    # whole app -- we degrade gracefully and tell the user search is down.
    retriever = None
    retriever_error = None
    try:
        retriever = get_retriever(k=4)
    except Exception as e:
        retriever_error = str(e)

    def search_guidelines(state: AgentState):
        log = state["steps_log"] + ["🔍 Searching clinical guidelines..."]
        if retriever is None:
            return {
                **state,
                "retrieved_chunks": [f"[Guideline search is currently unavailable: {retriever_error}]"],
                "steps_log": log,
            }
        try:
            docs = retriever.invoke(state["question"])
            chunks = [f"[{d.metadata['source']}] {d.page_content}" for d in docs]
        except Exception as e:
            chunks = [f"[Guideline search failed for this question: {e}]"]
        return {**state, "retrieved_chunks": chunks, "steps_log": log}

    graph = StateGraph(AgentState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("search_guidelines", search_guidelines)
    graph.add_node("check_labs", check_labs)
    graph.add_node("synthesize_answer", synthesize_answer)

    graph.set_entry_point("classify_intent")

    def route_after_classify(state):
        if state["needs_search"]:
            return "search_guidelines"
        elif state["needs_validation"]:
            return "check_labs"
        return "synthesize_answer"

    graph.add_conditional_edges("classify_intent", route_after_classify, {
        "search_guidelines": "search_guidelines",
        "check_labs": "check_labs",
        "synthesize_answer": "synthesize_answer",
    })
    graph.add_conditional_edges(
        "search_guidelines",
        lambda s: "check_labs" if s["needs_validation"] else "synthesize_answer",
        {"check_labs": "check_labs", "synthesize_answer": "synthesize_answer"},
    )
    graph.add_edge("check_labs", "synthesize_answer")
    graph.add_edge("synthesize_answer", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    print("=== TEST 1: Question + lab values ===\n")
    result = app.invoke({
        "question": "What is the target HbA1c for diabetes management, and is 7.1 too high?",
        "lab_values": {"HbA1c": 7.1}
    })
    print("Steps:", result["steps_log"])
    print("\nAnswer:\n", result["final_answer"])

    print("\n\n=== TEST 2: Question only, no lab values ===\n")
    result2 = app.invoke({
        "question": "What lifestyle changes help manage blood pressure in diabetic patients?",
        "lab_values": {}
    })
    print("Steps:", result2["steps_log"])
    print("\nAnswer:\n", result2["final_answer"])

    print("\n\n=== TEST 3: Second question, same process (Chroma fix still holds) ===\n")
    result3 = app.invoke({
        "question": "What is the normal LDL cholesterol range?",
        "lab_values": {}
    })
    print("Steps:", result3["steps_log"])
    print("\nAnswer:\n", result3["final_answer"])