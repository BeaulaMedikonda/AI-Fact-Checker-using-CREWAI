import os
from agents import build_crew
from dotenv import load_dotenv

load_dotenv()

# Prompt user for input
print("📌 Welcome to the Fact Checker!")
print("You can enter one of the following:")
print(" 1. A factual statement")
print(" 2. A website URL")
print(" 3. A YouTube video URL")

user_input = input("\n👉 Enter your input: ").strip()

# Detect input type
if user_input.startswith("http"):
    if "youtube.com" in user_input or "youtu.be" in user_input:
        input_data = {"input_youtube_url": user_input}
    else:
        input_data = {"input_url": user_input}
else:
    input_data = {"input_statement": user_input}

# Build and run the crew
crew = build_crew(input_data)
result = crew.kickoff(inputs=input_data)

# Final output
print("\n\n==== ✅ FACT-CHECK REPORT ====\n")
print(result)