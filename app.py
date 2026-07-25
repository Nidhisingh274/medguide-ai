import streamlit as st
from agent.graph import build_graph

st.set_page_config(page_title="MedGuide AI", page_icon="🩺", layout="centered")


@st.cache_resource
def load_agent():
    return build_graph()


app = load_agent()

st.title("🩺 MedGuide AI")
st.caption("Agentic clinical research & lab-value validation assistant — demo/portfolio project, not a medical device.")

st.subheader("Ask a question")
question = st.text_area(
    "Your clinical/medical question",
    placeholder="e.g. What is the target HbA1c for diabetes management?"
)

st.subheader("Optional: enter lab values to validate")
st.caption("Uses synthetic/sample values only — never enter real patient data.")

lab_test_options = [
    "Fasting Glucose", "HbA1c", "LDL Cholesterol",
    "HDL Cholesterol", "Triglycerides", "Systolic Blood Pressure"
]
col1, col2 = st.columns(2)
lab_values = {}
with col1:
    selected_tests = st.multiselect("Select lab tests to check", lab_test_options)
with col2:
    for test in selected_tests:
        val = st.number_input(f"{test} value", key=test, step=0.1)
        lab_values[test] = val

run_clicked = st.button("Ask MedGuide AI", type="primary")

if run_clicked:
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            with st.spinner("Working..."):
                result = app.invoke({"question": question, "lab_values": lab_values})
        except Exception as e:
            st.error(f"Something went wrong: {e}. Please try again.")
            st.stop()

        st.markdown("**Agent steps:**")
        for step in result["steps_log"]:
            st.write(step)

        st.markdown("---")
        st.subheader("Answer")
        st.write(result["final_answer"])

        if result.get("lab_results"):
            st.subheader("Lab Validation Detail")
            for r in result["lab_results"]:
                icon = {"normal": "✅", "high": "⚠️", "low": "⚠️", "unknown_test": "❓"}.get(r["status"], "•")
                st.write(f"{icon} {r['message']}")

        if result.get("retrieved_chunks"):
            with st.expander("Show retrieved guideline excerpts"):
                for chunk in result["retrieved_chunks"]:
                    st.markdown(f"> {chunk}")

with st.sidebar:
    st.header("About MedGuide AI")
    st.write("An agentic RAG assistant that answers clinical questions from ingested guidelines and validates lab values against reference ranges.")
    st.write("Built with LangGraph, Groq, Chroma, and Hugging Face embeddings.")
    st.markdown("[GitHub Repo](https://github.com/Nidhisingh274/medguide-ai)")
    st.caption("⚠️ Demo/portfolio project. Not a medical device. Uses public guidelines and synthetic lab data only.")

st.markdown("---")
st.caption("Built with Claude as part of the AB Talks 60-Day Claude AI Challenge.")