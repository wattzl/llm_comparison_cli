# LLM Comparison CLI Tool with Real Claude and Gemini API
# Requires: openai, anthropic, google-generativeai, python-dotenv

import os
import json
import gradio as gr
from openai import OpenAI
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup OpenAI
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Claude API Call ===
def get_claude_response(prompt):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-sonnet-20240229",  # or claude-3-opus-20240229 if you have access
            max_tokens=500,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"Claude Error: {e}"

# === Gemini API Call ===
def get_gemini_response(prompt):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini Error: {e}"

# === OpenAI GPT Response ===
def get_openai_response(prompt):
    try:
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI Error: {e}"

def list_gemini_models():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    models = genai.list_models()
    for model in models:
        print(model.name, model.supported_generation_methods)


# === Gradio Interface ===
def compare_llms(prompt):
    openai_reply = get_openai_response(prompt)
    claude_reply = get_claude_response(prompt)
    gemini_reply = get_gemini_response(prompt)

    return openai_reply, claude_reply, gemini_reply

iface = gr.Interface(
    fn=compare_llms,
    inputs=gr.Textbox(label="Enter your prompt"),
    outputs=[
        gr.Textbox(label="ChatGPT (OpenAI)"),
        gr.Textbox(label="Claude (Anthropic)"),
        gr.Textbox(label="Gemini (Google)")
    ],
    title="LLM Comparison Tool",
    description="Compare the responses from ChatGPT, Claude, and Gemini side by side."
)

if __name__ == "__main__":
    iface.launch()
