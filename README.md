# 🧠Aethra – Orchestrating Limitless Learning with AI Agents

The **Adaptive AI Tutor Orchestrator** is a smart backend system that personalizes learning experiences using emotional and cognitive feedback.  
It intelligently decides *how* to teach a concept - through flashcards, notes, or explanations - based on the student’s profile and emotional state.

---

## 🚀 Project Overview

This project aims to build an **AI-driven tutoring backend** that adapts dynamically to each learner.  
The orchestrator acts as the brain - analyzing student input, understanding intent, and selecting the right educational tool.

It also tracks **user mastery progress**, adjusts difficulty, and adds motivational personalization based on emotional state and learning style.  

---

## 🧩 Core Features

- **Dynamic Tool Orchestration:** Automatically routes queries to the right educational tool  
- **Emotion-Aware Adaptation:** Adjusts tone and pace depending on mood (confused, tired, focused)  
- **Learning-Style Personalization:** Custom tips for visual, auditory, and other learners  
- **Mastery Tracking:** Gradually updates user progress per topic  
- **Mock Tools Integration:** Includes flashcard, note, and explanation generators for testing  
- **FastAPI-Powered API:** Lightweight and fast backend for real-time orchestration  

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI  
- **Language:** Python 3.10+  
- **AI Logic:** Local LLM (via Ollama) for parameter extraction  
- **Libraries:** `httpx`, `pydantic`, `re`  
- **Mock Tools:** Simulated APIs for flashcards, notes, and explanations  

---

## 📂 Project Structure



## Project Structure

Aethra/
   
   ├─ services/
   
   │ └─ ai_logic.py            # LLM parameter extraction & defaults

   ├─ schemas/                 # JSON schemas for each tool

   ├─ prompts/                 # Prompt templates for LLM

   ├─ mocks/

   │ └─ mock_tools.py          # Mock endpoints for all tools

   ├─ main.py                  # FastAPI orchestrator backend

   ├─ test_extract.py          # LLM parameter extraction test

---

## Testing the Orchestrator

### Setup Instructions

# Clone the repository
git clone "https://github.com/atharvadeshmukh0024/Aethra.git"

cd Aethra

# Install Required Packages
pip install fastapi uvicorn

# Start mock tools server
Navigate to the mocks directory: \Aethra\mocks

Start the mock tools server:
python -m uvicorn mock_tools:mock_app --host 127.0.0.1 --port 9001 --reload

Open the docs to verify endpoints:
http://127.0.0.1:9001/docs

# Start orchestrator backend
Open a new terminal, navigate to the project root: \Aethra

Run the orchestrator backend:
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Open the docs to verify endpoints:
http://127.0.0.1:8000/docs

### Test Orchestrator

# Use Postman, curl, or any HTTP client to POST to:
POST http://127.0.0.1:8000/docs

1. Go to POST /orchestrate 

2. Enter sample JSON:

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


3. Click Execute.

4. Verify response contains:
   
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
  
  "formatted": "🤔 Don't worry, let me simplify: Here are your flashcards:\nQ1: derivatives?\nQ2: derivatives?\nQ3: derivatives?\nQ4: derivatives?\nQ5: derivatives?\n💡 (Tip: Try drawing a diagram for better understanding!)",
  
  "user_profile": {
  
    "name": "Alex",
    
    "learning_style": "visual",
    
    "mastery_level": 3,
    
    "emotional_state": "confused"
    
  },
  
  "updated_mastery": 1
  
}


# 📊 Check Mastery State

You can view how the system tracks progress using:

GET http://127.0.0.1:8000/state


### Example Output:
json
{
  "Alex": {
    "derivatives": 1.0
  }
}


---


👨‍💻 **Contributors**

- Team Members : Atharva Deshmukh, Prajwal Konde, Nakshatra Deshmukh

---

🏆 **Summary**

This project shows how an AI system can move beyond static answers and truly adapt to human learning behavior - changing tone, pacing, and teaching style dynamically.  
It’s a step toward emotionally intelligent digital tutoring for the next generation of learners.
