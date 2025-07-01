from flask import Flask, render_template, jsonify, request
import requests
import os
from supabase import create_client, Client
import uuid
from mistral_setup.llm import evaluate_answer 

app=Flask(__name__)


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.route("/start-interview", methods=["POST"])
def start_interview():
    data = request.json
    user_id = data.get("user_id")
    job_profile_id = data.get("job_profile_id")

    interview_id = str(uuid.uuid4())
    supabase.table("interviews").insert({
        "id": interview_id,
        "user_id": user_id,
        "job_profile_id": job_profile_id,
        "status": "ongoing"
    }).execute()

    question = supabase.table("questions") \
        .select("*") \
        .eq("job_profile_id", job_profile_id) \
        .order("order") \
        .limit(1).execute().data[0]

    return jsonify({
        "interview_id": interview_id,
        "question": question["question_text"],
        "question_id": question["id"]
    })

@app.route("/submit-response", methods=["POST"])
def submit_response():
    data = request.json
    interview_id = data["interview_id"]
    question_id = data["question_id"]
    transcript = data["transcript"]

    question = supabase.table("questions").select("question_text").eq("id", question_id).execute().data[0]
    eval_result = evaluate_answer(question["question_text"], transcript)

    # Optional: Parse score and feedback from eval_result if needed
    score = 8  # dummy placeholder — use regex if needed
    feedback = eval_result

    supabase.table("responses").insert({
        "interview_id": interview_id,
        "question_id": question_id,
        "transcript": transcript,
        "score": score,
        "feedback": feedback
    }).execute()

    return jsonify({"score": score, "feedback": feedback})

@app.route("/next-question", methods=["GET"])
def next_question():
    interview_id = request.args.get("interview_id")
    interview = supabase.table("interviews").select("*").eq("id", interview_id).execute().data[0]
    job_profile_id = interview["job_profile_id"]

    answered_ids = supabase.table("responses").select("question_id").eq("interview_id", interview_id).execute()
    answered_ids = [r["question_id"] for r in answered_ids.data]

    remaining = supabase.table("questions") \
        .select("*") \
        .eq("job_profile_id", job_profile_id) \
        .not_in("id", answered_ids) \
        .order("order") \
        .limit(1) \
        .execute().data

    if remaining:
        return jsonify({
            "question_id": remaining[0]["id"],
            "question": remaining[0]["question_text"]
        })
    else:
        return jsonify({"message": "Interview complete!"})

if __name__ == "__main__":
    app.run(debug=True)
