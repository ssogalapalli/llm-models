# Apply UI - using Gradio (Huggingface) for Frontier LLMs
# Tools feature:
#   Create a function and add in tool list so that LLM can call the function using tools feature
from connection.connect_openai import connect_openai
import gradio as gr  # To apply UI
import json

openai = connect_openai()
MODEL = "gpt-4o-mini"
# System prompt
system_message = "You are a helpful assistant for an Airline called KLM. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

# Ticket pricing function

ticket_prices = {"london" : "\N{euro sign}100", "bangalore" : "\N{euro sign}800","hyderabad" : "\N{euro sign}900"}
def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")


# There's a particular dictionary structure that's required to describe our function:

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

#defining global variable

booked_cities = []
def book_ticket(destination_city):
    print(f"Tool book_ticket called for {destination_city}")
    city = destination_city.lower()
    global booked_cities
    if city in ticket_prices:
        price = ticket_prices.get(city, "")
        label = f"{city.title()} ({price})"
        booked_cities.append(label)
        return f"Booking confirmed for {city.title()} at {ticket_prices[city]}"
    else:
        return "City not found in ticket prices."

book_function = {
    "name": "book_ticket",
    "description": "Book a ticket to the destination city. Call this whenever you want to book a ticket, for example when a customer want 'to book a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to book to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
# And this is included in a list of tools:

tools = [
    {"type": "function", "function": price_function},
    {"type": "function", "function": book_function}
]

#Define chat function
def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content

# We have to write that function handle_tool_call:
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

gr.ChatInterface(fn=chat, type="messages").launch()

