# LLM Comparison CLI Tool with Real Claude and Gemini API
# Requires: openai, anthropic, google-generativeai, python-dotenv

import os
import json
import csv
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

# Export to JSON file
def export_json():
    try:
        with open("comparison_result.json", "w", encoding="utf-8") as f:
            json.dump(comparison_result, f, ensure_ascii=False, indent=4)
        return "comparison_result.json"
    except Exception as e:
        return f"Error exporting JSON: {e}"

# Export to CSV file
# === CSV Export Helpers ===
def export_csv (prompt, response, model_name):
    filename = f"{model_name.lower().replace(' ', '_')}_output.csv"
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Prompt", "Response"])
            writer.writerow([prompt, response])
        return filename
    except Exception as e:
        return f"Error exporting CSV: {e}"

# === Gradio UI ===
# === Gradio UI ===
with gr.Blocks() as iface:
    gr.Markdown("# 🧠 LLM Comparison Tool")
    gr.Markdown("Compare responses from ChatGPT, Claude, and Gemini.")

    prompt_input = gr.Textbox(label="Enter your prompt", lines=2)
    submit_btn = gr.Button("Compare")

    def run_all_models(prompt):
        openai = get_openai_response(prompt)
        claude = get_claude_response(prompt)
        gemini = get_gemini_response(prompt)
        return openai, claude, gemini

    with gr.Row():
        with gr.Column():
            openai_output = gr.Textbox(label="ChatGPT", lines=6)
            openai_csv_btn = gr.Button("📄 Export CSV")
            openai_file = gr.File(interactive=False, visible=False)

        with gr.Column():
            claude_output = gr.Textbox(label="Claude", lines=6)
            claude_csv_btn = gr.Button("📄 Export CSV")
            claude_file = gr.File(interactive=False, visible=False)

        with gr.Column():
            gemini_output = gr.Textbox(label="Gemini", lines=6)
            gemini_csv_btn = gr.Button("📄 Export CSV")
            gemini_file = gr.File(interactive=False, visible=False)

    submit_btn.click(run_all_models, inputs=prompt_input, outputs=[openai_output, claude_output, gemini_output])

    openai_csv_btn.click(lambda p, r: export_csv(p, r, "chatgpt_output.csv"), inputs=[prompt_input, openai_output], outputs=openai_file)
    claude_csv_btn.click(lambda p, r: export_csv(p, r, "claude_output.csv"), inputs=[prompt_input, claude_output], outputs=claude_file)
    gemini_csv_btn.click(lambda p, r: export_csv(p, r, "gemini_output.csv"), inputs=[prompt_input, gemini_output], outputs=gemini_file)
if __name__ == "__main__":
    iface.launch()