import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DIR = "chroma_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REFERENCE_PATH = "data/lab_reference.csv"


def get_retriever(k=4):
    """
    Returns a retriever that searches the persisted Chroma vector store.
    k = number of chunks to return per query.
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": k})


def load_reference_table():
    return pd.read_csv(REFERENCE_PATH)


def validate_labs(test_values: dict):
    """
    test_values: dict like {"Fasting Glucose": 132, "HbA1c": 7.1}
    Returns a list of dicts, one per submitted test:
    {test_name, value, status, message}
    status is one of: "normal", "high", "low", "unknown_test"
    """
    ref = load_reference_table()
    results = []

    for test_name, value in test_values.items():
        row = ref[ref["test_name"].str.lower() == test_name.lower()]

        if row.empty:
            results.append({
                "test_name": test_name,
                "value": value,
                "status": "unknown_test",
                "message": f"No reference range found for '{test_name}'."
            })
            continue

        low = row.iloc[0]["low"]
        high = row.iloc[0]["high"]
        unit = row.iloc[0]["unit"]
        notes = row.iloc[0]["notes"]

        if value < low:
            status = "low"
            message = f"{test_name} is {value} {unit}, below the normal range ({low}-{high}). {notes}"
        elif value > high:
            status = "high"
            message = f"{test_name} is {value} {unit}, above the normal range ({low}-{high}). {notes}"
        else:
            status = "normal"
            message = f"{test_name} is {value} {unit}, within the normal range ({low}-{high})."

        results.append({
            "test_name": test_name,
            "value": value,
            "status": status,
            "message": message
        })

    return results


if __name__ == "__main__":
    print("=== Testing validate_labs() ===\n")
    sample = {"Fasting Glucose": 132, "HbA1c": 5.2, "LDL Cholesterol": 145, "Vitamin D": 30}
    for r in validate_labs(sample):
        print(f"{r['status'].upper():12} - {r['message']}")

    print("\n=== Testing get_retriever() still works ===\n")
    retriever = get_retriever(k=2)
    results = retriever.invoke("What is the target HbA1c?")
    for r in results:
        print(f"Source: {r.metadata['source']} (chunk {r.metadata['chunk_id']})")