# Apply UI - using Gradio (Huggingface) for Frontier LLMs
from connection.connect_openai import connect_openai
import gradio as gr  # To apply UI

openai = connect_openai()
MODEL = "gpt-4o-mini"
# System prompt
system_message = "You are a helpful assistant for an Airline called KLM. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

#define chat function

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

# Launch Gradio UI
gr.ChatInterface(fn=chat, type="messages").launch()





