import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert technical interviewer. 
Your goal is to assess the candidate's backend engineering skills.
Keep your responses concise (under 2 sentences) and conversational.
Do not write code blocks, just speak naturally.
Start by asking them to introduce themselves."""

async def get_ai_response(transcript: str, conversation_history: list):
    conversation_history.append({"role": "user", "content": transcript})
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ],
        temperature=0.6,
        max_tokens=150,
    )
    
    response_text = completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response_text})
    return response_text, conversation_history