import os
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv

# Load the OpenAI API key from the .env file
load_dotenv()

openai = OpenAI()

def generate_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that always responds in markdown."},
        {"role": "user", "content": prompt}
    ]
    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages, 
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=10, placeholder="Type your prompt here..."),
    outputs=gr.Markdown(),
    title="GPT-4 Prompt Generator",
    description="Enter a prompt and get a response from GPT-4"
)

iface.launch()