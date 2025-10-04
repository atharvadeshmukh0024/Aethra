from services.ai_logic import extract_params

msg = "I need 5 easy practice problems on derivatives in calculus"
user_profile = {"name":"Alex","learning_style":"visual","emotional_state":"confused","mastery_level":3}

result = extract_params("flashcard_generator", msg, [], user_profile)
print(result)
