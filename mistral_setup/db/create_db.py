import uuid
from supabase_client import supabase

def seed_job_profile(name):
    profile_id = str(uuid.uuid4())
    supabase.table("job_profiles").insert({
        "id": profile_id,
        "job_name": name
    }).execute()
    return profile_id

def seed_questions(job_profile_id, questions, answer):
    for order, question in enumerate(questions, start=1):
        supabase.table("questions").insert({
            "id": str(uuid.uuid4()),
            "job_profile_id": job_profile_id,
            "order": order,
            "question_text": question,
            "verfied_answer": answer
        }).execute()

def seed_user_answers(question_id, useranswers):
    for order, answer in enumerate(useranswers, start=1):
        supabase.table("user_answers").insert({
            "id": str(uuid.uuid4()),
            "question_id": question_id,
            ""
            "answer_text": answer
        }).execute()


def main():
    print("Seeding job profiles and questions...")

    # --- Frontend Developer ---
    frontend_questions = [
        "Tell me about yourself.",
        "What is the difference between == and === in JavaScript?",
        "How does the virtual DOM work in React?",
        "What are React hooks and how do you use them?",
        "Explain how you would optimize performance in a large React application.",
        "What is closure in JavaScript?",
        "How do you handle state management in a React app?"
    ]
    frontend_id = seed_job_profile("Frontend Developer")
    seed_questions(frontend_id, frontend_questions)

    # --- Backend Developer ---
    backend_questions = [
        "Tell me about yourself.",
        "What is REST API and how does it work?",
        "What is the difference between synchronous and asynchronous programming?",
        "How do you handle authentication and authorization in Flask?",
        "What is the difference between SQL and NoSQL databases?",
        "What is an ORM and why would you use it?",
        "How would you design a scalable backend system for millions of users?"
    ]
    backend_id = seed_job_profile("Backend Developer")
    seed_questions(backend_id, backend_questions)

    print("✅ Done seeding.")

if __name__ == "__main__":
    main()
