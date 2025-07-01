import os
from dotenv import load_dotenv
import requests




load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

def evaluate_answer(question, answer):
    prompt = f"""
        You are an AI interviewer evaluating candidate responses.

        Question: "{question}"
        Answer: "{answer}"

        Give:
        1. Score (1–10)
        2. Feedback (2-3 lines)
        """
    
    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small",  # or "mixtral-8x7b-32768"
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)

    print(response.json()['choices'][0]['message']['content'])
    return response

if __name__ == "__main__":
    question = "What is your greatest strength?"
    answer = "I am a quick learner and adapt to new environments easily."
    evaluate_answer(question, answer) 