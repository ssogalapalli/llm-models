from connection.connect_ollama import connect_ollama

ollama_connect_openai = connect_ollama()

HEADERS = {"Content-Type": "application/json"}
MODEL = " llama3.2"
messages =[
    {"role": "user", "content": "Write an email to request for new resources in the team"}
]

response = ollama_connect_openai.chat.completions.create(
    model=MODEL,
    messages=messages
)

print(response.choices[0].message.content)

