from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model + tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("📦 Model loaded successfully!")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    output = model.generate(input_ids, max_length=100, do_sample=True, top_k=50)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Remove the original prompt from the response
    bot_reply = response[len(user_input):].strip()
    print("Bot:", bot_reply)
