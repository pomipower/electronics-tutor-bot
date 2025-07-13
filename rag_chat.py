import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ==== Settings ====
COLLECTIONS = [
    "EEE_11th_Edition_Electronic_Devices_and_Circuit_Theory",
    "EEE_R_P_JainDigital_Electronics_text_book_1"
]
VECTOR_DB_PATH = "vector_db"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "microsoft/phi-2"
TOP_K = 2
MAX_TOKENS = 200

# ==== Load models ====
print("🧠 Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL_NAME)

print("🤖 Loading model (this may take a minute)...")
# 🔁 Detect GPU or fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print("🤖 Using device:", device)

# 🔁 Load Phi-2 on GPU
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME)
model = model.to(device)  # 🚀 Send model to GPU
model.config.pad_token_id = tokenizer.eos_token_id



# ==== Load vector database ====
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collections = [client.get_collection(name=name) for name in COLLECTIONS]

# ==== Main chatbot loop ====
print("\n⚡ RAG-powered Electronics Tutor")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break

    # 1. Embed user query
    query_vec = embedder.encode(user_input)

    # 2. Retrieve from all collections
    results = []
    for collection in collections:
        retrieved = collection.query(query_embeddings=[query_vec], n_results=TOP_K)
        docs = retrieved["documents"][0]
        metas = retrieved["metadatas"][0]
        results.extend(zip(docs, metas))

    # 3. Select top combined results
    top_chunks = results[:TOP_K]

    # 4. Format prompt
    context = "\n".join([f"{i+1}. {chunk[0]}" for i, chunk in enumerate(top_chunks)])
    prompt = (
        "You are an expert electronics tutor. Use the following reference material to answer the question.\n\n"
        "REFERENCE:\n"
        f"{context}\n\n"
        f"QUESTION: {user_input}\n"
        f"EXPLANATION:"
    )

    #print("\n📚 Retrieved context:")
    #print(context)

    # 5. Generate answer
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    output = model.generate(
        **inputs,
        max_new_tokens=MAX_TOKENS,
        max_length=inputs["input_ids"].shape[1] + MAX_TOKENS,
        temperature=0.7,
        top_k=50,
        do_sample=True
    )

    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    final_reply = reply[len(prompt):].strip().split("\n")[0]

    print(f"\n🤖 Bot: {final_reply}\n")
