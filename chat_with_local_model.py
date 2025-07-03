from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import difflib

# Load model + tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("📦 Model loaded successfully!")

# Pad token config to avoid warnings
model.config.pad_token_id = model.config.eos_token_id

# Simple FAQ database
faq = {
    "what is a diode": "A diode is a component that allows current to flow in only one direction. It's used for rectification and protection.",
    "what is a transistor": "A transistor is a semiconductor device used to amplify or switch electronic signals.",
    "what is an inductor": "An inductor is a passive component that stores energy in a magnetic field when current flows through it.",
    "what is voltage": "Voltage is the electrical potential difference between two points. It's what pushes current through a circuit.",
    "what is current": "Current is the flow of electric charge in a conductor, measured in amperes (A).",
    "series vs parallel circuits": "In series circuits, components share the same current. In parallel circuits, they share the same voltage.",
    "what is resistance": "Resistance is the opposition to current flow in an electrical circuit. It's measured in ohms (Ω).",
    "what is power in circuits": "Power (P) in a circuit is the rate at which energy is used, calculated as P = V × I.",
}

# 🔧 Core function to reuse for CLI or GUI
def get_bot_reply(user_input):
    # Clean user input
    query = user_input.lower().strip("?!. ")

    # Try FAQ fuzzy match
    match = difflib.get_close_matches(query, faq.keys(), n=1, cutoff=0.6)
    if match:
        matched_question = match[0]
        reply = faq[matched_question]
        source = f"faq (matched '{matched_question}')"
        return reply, source

    # Prepare prompt for LLM
    prompt = (
        "You are an expert electronics tutor. Your job is to explain concepts clearly and simply.\n\n"
        f"Question: {user_input}\n"
        "Answer:"
    )
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    # Generate response
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=60,
        do_sample=True,
        top_k=40,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract answer portion
    reply = response[len(prompt):].strip().split("\n")[0]
    if len(reply) < 15:
        reply = "Sorry, I didn't quite understand that. Try rephrasing your question."

    return reply, "llm"

# 🖥️ Command-Line Chat Loop (can be reused for testing even after GUI)
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        reply, source = get_bot_reply(user_input)
        print(f"Bot ({source}):", reply)

        # Log to file
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{source}] You: {user_input}\nBot: {reply}\n\n")
