import html
import streamlit as st
from agent.graph import build_graph

st.set_page_config(page_title="MedGuide AI", page_icon="🩺", layout="wide")

CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 880px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .mg-hero {
        background: linear-gradient(135deg, #0B2E33 0%, #028090 100%);
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 28px;
        color: white;
    }
    .mg-hero h1 {
        margin: 0 0 6px 0;
        font-size: 2rem;
        color: white;
    }
    .mg-hero p {
        margin: 0;
        color: #CADCFC;
        font-size: 0.95rem;
    }
    .mg-card {
        background: #F4FAF9;
        border: 1px solid #E0EEEC;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .mg-step-pill {
        display: inline-block;
        background: #E6F7F3;
        color: #015A64;
        border: 1px solid #02C39A;
        border-radius: 999px;
        padding: 6px 14px;
        margin: 4px 6px 4px 0;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .mg-source-badge {
        display: inline-block;
        background: #0B2E33;
        color: white;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-family: monospace;
        margin-bottom: 6px;
    }
    .mg-excerpt {
        background: white;
        border-left: 3px solid #02C39A;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 12px;
        font-size: 0.88rem;
        color: #3D4E4C;
        white-space: pre-wrap;
    }
    .mg-lab-normal, .mg-lab-flag, .mg-lab-unknown {
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.92rem;
    }
    .mg-lab-normal { background: #EAFBF4; border-left: 4px solid #02C39A; color: #0B2E33; }
    .mg-lab-flag { background: #FFF4E5; border-left: 4px solid #E8871E; color: #5C3A0A; }
    .mg-lab-unknown { background: #F2F2F2; border-left: 4px solid #999; color: #444; }
    .mg-footer {
        text-align: center;
        color: #4F6863;
        font-size: 0.8rem;
        padding-top: 18px;
        margin-top: 30px;
        border-top: 1px solid #E0EEEC;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def load_agent():
    return build_graph()


try:
    app = load_agent()
    agent_load_failed = False
except Exception as e:
    agent_load_failed = True
    agent_load_error = str(e)

# ---------- Hero header ----------
st.markdown("""
<div class="mg-hero">
    <h1>🩺 MedGuide AI</h1>
    <p>Agentic clinical research & lab-value validation assistant — demo/portfolio project, not a medical device.</p>
</div>
""", unsafe_allow_html=True)

if agent_load_failed:
    st.error(
        f"MedGuide AI couldn't start up correctly ({agent_load_error}). "
        "This is usually a temporary configuration issue on our end — please try refreshing in a minute. "
        "If it persists, the site owner needs to check the Groq API key or vector store setup."
    )
    st.stop()

# ---------- Session state for example-question prefill ----------
if "question_box" not in st.session_state:
    st.session_state.question_box = ""

EXAMPLE_QUESTIONS = [
    "What is the target HbA1c for diabetes management?",
    "What lifestyle changes help manage blood pressure in diabetic patients?",
    "What are the risks of uncontrolled LDL cholesterol?",
]

st.markdown("**Ask a question**")
st.caption("New here? Try one of these, or write your own below:")

chip_cols = st.columns(len(EXAMPLE_QUESTIONS))
for i, ex in enumerate(EXAMPLE_QUESTIONS):
    with chip_cols[i]:
        if st.button(ex, key=f"chip_{i}", use_container_width=True):
            st.session_state.question_box = ex
            st.rerun()

question = st.text_area(
    "Your clinical/medical question",
    placeholder="e.g. What is the target HbA1c for diabetes management?",
    key="question_box",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**Optional: enter lab values to validate**")
st.caption("Uses synthetic/sample values only — never enter real patient data.")

lab_test_options = [
    "Fasting Glucose", "HbA1c", "LDL Cholesterol",
    "HDL Cholesterol", "Triglycerides", "Systolic Blood Pressure"
]
col1, col2 = st.columns(2)
lab_values = {}
missing_values = []
with col1:
    selected_tests = st.multiselect("Select lab tests to check", lab_test_options, label_visibility="collapsed", placeholder="Select lab tests to check")
with col2:
    for test in selected_tests:
        # value=None (not 0.0) so an untouched field is detectable and never
        # silently treated as a real "0" reading.
        val = st.number_input(f"{test} value", key=test, step=0.1, value=None, placeholder="Enter value")
        if val is None:
            missing_values.append(test)
        else:
            lab_values[test] = val

run_clicked = st.button("Ask MedGuide AI", type="primary")

if run_clicked:
    if not question.strip():
        st.warning("Please enter a question first.")
    elif missing_values:
        st.warning(f"Please enter a value for: {', '.join(missing_values)} (or remove it from the selected tests).")
    else:
        try:
            with st.spinner("MedGuide AI is working through your question..."):
                result = app.invoke({"question": question, "lab_values": lab_values})
        except Exception as e:
            error_text = str(e).lower()
            if "connection" in error_text or "timeout" in error_text or "network" in error_text:
                st.error("Couldn't reach the AI service — this looks like a network issue. Please check your connection and try again.")
            else:
                st.error(f"Something went wrong: {e}. Please try again.")
            st.stop()

        step_pills = "".join([f'<span class="mg-step-pill">{html.escape(s)}</span>' for s in result["steps_log"]])
        st.markdown(f"<div>{step_pills}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="mg-card">', unsafe_allow_html=True)
        st.markdown("### Answer")
        st.write(result["final_answer"])
        st.markdown('</div>', unsafe_allow_html=True)

        if result.get("lab_results"):
            st.markdown("### Lab Validation Detail")
            for r in result["lab_results"]:
                if r["status"] == "normal":
                    css_class, icon = "mg-lab-normal", "✅"
                elif r["status"] == "unknown_test":
                    css_class, icon = "mg-lab-unknown", "❓"
                else:
                    css_class, icon = "mg-lab-flag", "⚠️"
                st.markdown(f'<div class="{css_class}">{icon} {html.escape(r["message"])}</div>', unsafe_allow_html=True)

        if result.get("retrieved_chunks"):
            with st.expander("📚 Show retrieved guideline excerpts"):
                for chunk in result["retrieved_chunks"]:
                    if "]" in chunk:
                        source, text = chunk.split("]", 1)
                        source = source.replace("[", "")
                    else:
                        source, text = "source", chunk
                    st.markdown(f'<span class="mg-source-badge">{html.escape(source)}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mg-excerpt">{html.escape(text.strip())}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("About MedGuide AI")
    st.write("An agentic RAG assistant that answers clinical questions from ingested guidelines and validates lab values against reference ranges.")
    st.write("**Built with:** LangGraph, Groq, Chroma, Hugging Face embeddings")
    st.markdown("[🔗 GitHub Repo](https://github.com/Nidhisingh274/medguide-ai)")
    st.warning("Demo/portfolio project. Not a medical device. Uses public guidelines and synthetic lab data only.")

st.markdown(
    '<div class="mg-footer">Built with Claude as part of the AB Talks 60-Day Claude AI Challenge.</div>',
    unsafe_allow_html=True,
)