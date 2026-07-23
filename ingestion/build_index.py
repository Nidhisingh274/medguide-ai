import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_DIR = "data/raw_pdfs"

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

if __name__ == "__main__":
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    print(f"\nTotal chunks created: {len(chunks)}")
    print("\n--- Sample chunk ---")
    print(chunks[0]["source"], "| chunk", chunks[0]["chunk_id"])
    print(chunks[0]["text"][:300])