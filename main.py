from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import re
   


app = FastAPI()
# Simple in-memory state store
user_mastery = {}


# Input format for /orchestrate
class UserProfile(BaseModel):
    name: str = "Student"
    learning_style: str = "visual"
    mastery_level: int = 3
    emotional_state: str = "focused"

class OrchestrateInput(BaseModel):
    message: str
    user_profile: UserProfile
# Simple in-memory state store
user_mastery = {}

def update_mastery(user_profile: dict, topic: str, mood: str):
    """
    Update the mastery level for a user based on topic and emotional state.
    - If user is confused → slower progress
    - Otherwise → increment mastery
    """
    name = user_profile.get("name", "Unknown")
    if name not in user_mastery:
        user_mastery[name] = {}

    if topic not in user_mastery[name]:
        user_mastery[name][topic] = 0

    # Update rule
    if mood == "confused":
        user_mastery[name][topic] += 0.5  # slower growth
    else:
        user_mastery[name][topic] += 1

    return user_mastery[name][topic]


    
def personalize_response(tool_response: dict, user_profile: dict) -> str:
    """
    Personalizes the final formatted answer based on learning style + emotional state.
    """
    base_output = ""

    # Handle different tools
    if tool_response.get("tool") == "flashcard_generator":
        flashcards = tool_response.get("flashcards", [])
        base_output = "Here are your flashcards:\n" + "\n".join(flashcards)

    elif tool_response.get("tool") == "note_maker":
        base_output = tool_response.get("notes", "")
    elif tool_response.get("tool") == "concept_explainer":
        base_output = tool_response.get("explanation", "")

    # Personalize based on learning style
    style = user_profile.get("learning_style", "visual")
    if style == "visual":
        base_output += "\n💡 (Tip: Try drawing a diagram for better understanding!)"
    elif style == "auditory":
        base_output += "\n🔊 (Tip: Read this out loud or listen to an audio version!)"

    # Personalize based on emotional state
    mood = user_profile.get("emotional_state", "focused")
    if mood == "tired":
        base_output = "😌 Take it easy! Here's a lighter explanation: " + base_output
    elif mood == "confused":
        base_output = "🤔 Don't worry, let me simplify: " + base_output
    elif mood == "focused":
        base_output = "🎯 Great focus! Here’s the content: " + base_output

    return base_output

    
def extract_count(message: str, fallback: int = 3):
    """
    Extracts the first number mentioned in the message.
    Example: "Give me 5 flashcards" -> 5
    If no number found, return fallback (default = 3).
    """
    numbers = re.findall(r"\d+", message)
    if numbers:
        return int(numbers[0])
    return fallback
    
def extract_topic(message: str, fallback: str = "general"):
    """
    Very simple keyword-based extractor:
    - Picks the last word(s) after 'on' or 'about' or 'explain'
    - If nothing found, returns fallback
    """
    message = message.lower()
    if " on " in message:
        return message.split(" on ")[-1].strip()
    elif " about " in message:
        return message.split(" about ")[-1].strip()
    elif " explain " in message:
        return message.split("explain")[-1].strip()
    else:
        return fallback

@app.get("/")
def read_root():
    return {"status": "running", "message": "AI Tutor Orchestrator backend is live 🚀"}

@app.get("/state")
def get_state():
    """
    Returns the full mastery state of all students.
    """
    return user_mastery

# Main endpoint
@app.post("/orchestrate")
async def orchestrate(input: OrchestrateInput):
    message = input.message.lower()

    # Tool selection based on keywords
    if "note" in message:
        tool = "note_maker"
        endpoint = "http://127.0.0.1:9001/note"
        payload = {"topic": extract_topic(message, "general")}

    elif "flashcard" in message or "practice" in message:
        tool = "flashcard_generator"
        endpoint = "http://127.0.0.1:9001/flashcard"
        payload = {
            "topic": extract_topic(message, "general"),
            "count": extract_count(message, 3)
        }

    elif "explain" in message or "explanation" in message:
        tool = "concept_explainer"
        endpoint = "http://1 27.0.0.1:9001/explain"
        payload = {"topic": extract_topic(message, "general")}

    else:
        return {"error": "No matching tool found"}

    # Call the selected tool
    
    # Track mastery level updates
    topic = payload.get("topic", "general")
    new_mastery = update_mastery(input.user_profile.dict(), topic, input.user_profile.emotional_state)

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=payload)
        tool_response = response.json()

    formatted = personalize_response(tool_response, input.user_profile.dict())

    return {
    "tool": tool,
    "params": payload,
    "tool_response": tool_response,
    "formatted": formatted,
    "user_profile": input.user_profile.dict(),
    "updated_mastery": new_mastery
}
