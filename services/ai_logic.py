import os, json, re
import requests
from jsonschema import validate, ValidationError

def extract_params(tool, message, chat_history, user_profile):
    # If tool is "auto", let LLM decide
    is_auto = False
    if tool == "auto":
        is_auto = True
        tool = "flashcard_generator"  # temporary fallback for schema loading

    # Load schema for the tool
    schema_path = f"schemas/{tool}.json"
    schema = json.load(open(schema_path))

    # Build prompt
    prompt_template = open("prompts/param_extraction_prompt.txt").read()
    prompt = prompt_template.replace("<<MESSAGE>>", message)
    prompt = prompt.replace("<<CHAT_HISTORY>>", json.dumps(chat_history))
    prompt = prompt.replace("<<USER_PROFILE>>", json.dumps(user_profile))

    # Call local Ollama model
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        raw = resp.json().get("response", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw, re.S)
        if match:
            data = json.loads(match.group())
        else:
            raise Exception(f"LLM did not return valid JSON: {raw}")

    except Exception as e:
        print("Error calling Ollama:", e)
        data = {}

    # Validate against schema
    try:
        validate(instance=data, schema=schema)
    except ValidationError:
        data = apply_defaults(tool, data, user_profile)

    # Fill missing required fields
    data = apply_defaults(tool, data, user_profile)

    # If tool was auto, overwrite with LLM-decided tool
    if is_auto and "tool" in data:
        tool = data["tool"]

    data["tool"] = tool
    return data


def apply_defaults(tool, data, user_profile):
    """Fill in missing values safely"""
    if tool == "flashcard_generator":
        data.setdefault("topic", "general")
        data.setdefault("subject", "general")
        data.setdefault("count", 5)
        data.setdefault("difficulty", "easy")
    elif tool == "note_maker":
        data.setdefault("topic", "general")
        data.setdefault("subject", "general")
        data.setdefault("length", "short")
    elif tool == "concept_explainer":
        data.setdefault("topic", "general")
        data.setdefault("subject", "general")
        data.setdefault("style", user_profile.get("learning_style", "direct"))
    data.setdefault("user_info", user_profile)
    return data
