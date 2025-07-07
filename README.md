# ⚡ Electronics Tutor Bot (Offline)

A simple offline chatbot that answers basic electronics questions using:
- A local GPT-2 language model (Hugging Face Transformers)
- A built-in Q&A database with fuzzy matching
- A simple web UI built with Streamlit

---

## 🚀 Features

- Fully offline after initial setup
- Smart fallback: uses memory for known questions, GPT-2 for unknowns
- Clean UI and CLI support
- Logs chat history in `chat_log.txt`

---

## 🧠 Sample Questions

Try asking:

- What is Ohm's Law?
- Difference between AC and DC
- What is a capacitor?
- Explain Kirchhoff's Voltage Law

---

## 💻 How to Run

```bash
git clone https://github.com/<your-username>/electronics-tutor-bot
cd electronics-tutor-bot

# Set up virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run chatbot (terminal version)
python chat_with_local_model.py

# OR launch the web version
streamlit run electronics_tutor_gui.py
