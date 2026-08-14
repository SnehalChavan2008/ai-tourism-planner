import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.5-flash")

def generate_itinerary(destination, days, budget, travelers, interests, place):

    prompt = f"""
    Create a {days} day travel itinerary.

    Destination : {destination}
    State : {place['state']}
    Budget : ₹{budget}
    Travelers : {travelers}

    Interests:
    {", ".join(interests)}

    Tourist Attractions:
    {place['attractions']}

    Write itinerary like this:

    Day 1
    Morning
    Afternoon
    Evening

    Day 2
    Morning
    Afternoon
    Evening

    Continue till Day {days}.

    Also include approximate budget.
    """

    response = model.generate_content(prompt)

    return response.text

# ---------------- AI CHATBOT ----------------

def chat_with_ai(question, destination):

    prompt = f"""
    You are an AI Travel Assistant.

    The user is planning a trip to {destination}.

    Answer the user's question clearly and helpfully.

    Destination: {destination}

    User Question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text

