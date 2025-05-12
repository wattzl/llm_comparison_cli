# 🧠 LLM Comparison Tool

A simple and interactive UI to compare responses from:

- **ChatGPT (OpenAI)**
- **Claude (Anthropic)**
- **Gemini (Google)**

Built with **Python** and **Gradio** for fast prototyping and experimentation.

---

## 🚀 Features

- Prompt input via UI
- Real-time responses from all 3 LLMs
- Side-by-side output comparison
- Supports `.env`-based API key loading

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt


🔐 .env Setup

Create a .env file in the root folder:

OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=your_gemini_api_key

▶️ Running the App

python llm_comparison_cli.py

📁 Project Structure

llm-comparison-cli/
├── llm_comparison_cli.py
├── .env
├── requirements.txt
└── README.md

🧑‍💻 Author

Built by [wattzl] — powered by OpenAI, Anthropic, and Google APIs.