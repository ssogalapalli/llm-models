from connection.connect_openai import connect_openai


messages = [
    {"role": "system", "content": "You're an assistant to write email"},
    {"role": "user", "content": "Write an email to request for new resources in the team"}
]

openai = connect_openai()
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
print(response.choices[0].message.content)

