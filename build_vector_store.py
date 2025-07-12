import os
import json
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Settings (Change BOOK_NAME as per extracted_text json name, to add different books)
BOOK_NAME = "EEE_R_P_JainDigital_Electronics_text_book_1"
INPUT_FILE = f"extracted_text/{BOOK_NAME}.json"
DB_FOLDER = "vector_db"

# 2. Load textbook pages
def load_json_pages(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        pages = json.load(f)
    return pages

# 3. Chunk paragraphs smartly
def chunk_text(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    all_chunks = []
    for page in pages:
        paragraphs = page["text"].split("\n\n")  # crude paragraph split
        for para in paragraphs:
            para = para.strip()
            if len(para) < 100:
                continue  # skip short ones
            chunks = text_splitter.split_text(para)
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "page": page["page"]
                })
    return all_chunks

# 4. Embed and store in vector DB (Chroma)
def embed_and_store(chunks, book_name, persist_dir=DB_FOLDER):
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Init Chroma
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name=book_name)

    # Prepare and insert
    for i, chunk in tqdm(enumerate(chunks), total=len(chunks)):
        embedding = model.encode(chunk["text"])
        metadata = {"page": chunk["page"]}
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[f"{book_name}_{i}"]
        )

    print(f"✅ Stored {len(chunks)} chunks in vector DB at: {persist_dir}")

# 5. Run all steps
if __name__ == "__main__":
    pages = load_json_pages(INPUT_FILE)
    print(f"📘 Loaded {len(pages)} pages from {BOOK_NAME}")

    chunks = chunk_text(pages)
    print(f"✂️ Created {len(chunks)} chunks")

    embed_and_store(chunks, book_name=BOOK_NAME)
