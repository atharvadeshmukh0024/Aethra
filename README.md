# AI Tutor Orchestrator – Checkpoint 1

## Project Status
Backend Orchestrator functional with mock tools

## Completed Features
- Backend built using FastAPI with `/orchestrate` endpoint
- Parameter extraction from student messages using local LLM (Ollama LLaMA 3.2)
- Integration with three mock educational tools:
  - Flashcard Generator
  - Note Maker
  - Concept Explainer
- Personalized responses based on learning style and emotional state
- Mastery tracking for each student and topic
- Fully tested with sample messages, outputs verified

## Project Structure

Aethra/
   
   ├─ services/
   
   │ └─ ai_logic.py # LLM parameter extraction & defaults

   ├─ schemas/ # JSON schemas for each tool

   ├─ prompts/ # Prompt templates for LLM

   ├─ mocks/

   │ └─ mock_tools.py # Mock endpoints for all tools

   ├─ main.py # FastAPI orchestrator backend

   ├─ test_extract.py # LLM parameter extraction test


## Checkpoint Status
- Backend orchestration logic: Completed
- Tool integration with LLM: Completed (using mocks)
- Personalization & mastery tracking: Completed



## Testing the Orchestrator

### Setup Instructions

# Clone the repository
git clone <repo-url>
cd Aethra

# Install dependencies
pip install fastapi uvicorn httpx pydantic jsonschema requests

# Start mock tools server
uvicorn mock_tools:mock_app --host 127.0.0.1 --port 9001 --reload

# Start orchestrator backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

### Test Orchestrator

# Use Postman, curl, or any HTTP client to POST to:
POST http://127.0.0.1:8000/orchestrate

# Body (JSON):
{
    "message": "Give me 5 flashcards on derivatives",
    "user_profile": {
        "name": "Alex",
        "learning_style": "visual",
        "mastery_level": 3,
        "emotional_state": "confused"
    }
}

# Sample Response:
{
  "tool": "flashcard_generator",
  "params": {
    "topic": "derivatives",
    "count": 5
  },
  "tool_response": {
    "tool": "flashcard_generator",
    "flashcards": [
      "Q1: derivatives?",
      "Q2: derivatives?",
      "Q3: derivatives?",
      "Q4: derivatives?",
      "Q5: derivatives?"
    ]
  },
  "formatted": "Don't worry, let me simplify: Here are your flashcards:\nQ1: derivatives?\nQ2: derivatives?\nQ3: derivatives?\nQ4: derivatives?\nQ5: derivatives?\n(Tip: Try drawing a diagram for better understanding!)",
  "user_profile": {
    "name": "Alex",
    "learning_style": "visual",
    "mastery_level": 3,
    "emotional_state": "confused"
  },
  "updated_mastery": 1
}
