import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

RAW_DIR = "data/raw_pdfs"
CHROMA_DIR = "chroma_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_pdf_text(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text


def load_all_documents():
    documents = []
    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(RAW_DIR, filename)
            text = load_pdf_text(path)
            documents.append({"source": filename, "text": text})
            print(f"Loaded {filename}: {len(text)} characters")
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["text"])
        for i, chunk_text in enumerate(splits):
            chunks.append({"source": doc["source"], "chunk_id": i, "text": chunk_text})
    return chunks


def build_vector_store(chunks):
    print("\nLoading embedding model (first run downloads it, may take a minute)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    docs = [
        Document(page_content=c["text"], metadata={"source": c["source"], "chunk_id": c["chunk_id"]})
        for c in chunks
    ]

    print(f"Embedding and storing {len(docs)} chunks in Chroma...")
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"Stored {len(docs)} chunks in Chroma at '{CHROMA_DIR}'")
    return vectordb


if __name__ == "__main__":
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    print(f"\nTotal chunks: {len(chunks)}")

    vectordb = build_vector_store(chunks)

    print("\n--- Test query ---")
    test_query = "What is the target HbA1c for diabetes management?"
    results = vectordb.similarity_search(test_query, k=3)
    print(f"Query: {test_query}\n")
    for i, r in enumerate(results):
        print(f"[{i+1}] Source: {r.metadata['source']} (chunk {r.metadata['chunk_id']})")
        print(r.page_content[:200])
        print()