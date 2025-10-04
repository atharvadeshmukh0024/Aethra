from fastapi import FastAPI
from pydantic import BaseModel

mock_app = FastAPI()

# Flashcard Tool
class FlashcardInput(BaseModel):
    topic: str
    count: int

@mock_app.post("/flashcard")
async def flashcard(input: FlashcardInput):
    return {
        "tool": "flashcard_generator",
        "flashcards": [f"Q{i+1}: {input.topic}?" for i in range(input.count)]
    }

# Note Maker Tool
class NoteInput(BaseModel):
    topic: str

@mock_app.post("/note")
async def note_maker(input: NoteInput):
    return {
        "tool": "note_maker",
        "notes": f"Here are some quick notes on {input.topic}."
    }

# Concept Explainer Tool
class ExplainInput(BaseModel):
    topic: str

@mock_app.post("/explain")
async def concept_explainer(input: ExplainInput):
    return {
        "tool": "concept_explainer",
        "explanation": f"Let me explain {input.topic} in a simple way..."
    }
