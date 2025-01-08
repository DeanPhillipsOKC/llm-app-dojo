import gradio as gr
from openai import OpenAI
import json

openai = OpenAI()

ticket_prices = {
    "london": "$799",
    "paris": "$899",
    "tokyo": "$1400",
    "berlin": "$499"
}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": message.tool_calls[0].id
    }

    return response, city

def airline_assistant(message, history):
    messages = [
        {
            "role": "system", 
            "content": """You are a helpful assistant for an airline called FlightAI.
                Give short, courteous answers, no more than 1 sentence.
                Always be accurate.  If you don't know the answer, say so."""
        }
    ]

    for user_message, assistant_message in history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "system", "content": assistant_message})
    messages.append({"role": "user", "content": message})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)

    return response.choices[0].message.content

price_function = {
    "name": "get_ticket_price",
    "description": (
        "Get the price of a return ticket to the destination city. "
        "Call this whenever you need to know the ticket price. "
        "For example, 'What is the price of a ticket to London?'"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city the customer wants to fly to"
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

gr.ChatInterface(fn=airline_assistant).launch()