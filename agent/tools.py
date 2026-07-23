from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DIR = "chroma_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_retriever(k=4):
    """
    Returns a retriever that searches the persisted Chroma vector store.
    k = number of chunks to return per query.
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    retriever = get_retriever(k=3)
    test_query = "What lifestyle changes help manage blood pressure in diabetic patients?"
    results = retriever.invoke(test_query)
    print(f"Query: {test_query}\n")
    for i, r in enumerate(results):
        print(f"[{i+1}] Source: {r.metadata['source']} (chunk {r.metadata['chunk_id']})")
        print(r.page_content[:200])
        print()
        