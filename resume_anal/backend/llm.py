import json
from dotenv import load_dotenv
import os
import requests
import textstat
import spacy

load_dotenv()
api_key=os.getenv("MISTRAL_API_KEY")

def get_res(resume,jd):
    prompt=f"""
You are an expert career advisor, resume coach, and AI-powered evaluator.

A user has submitted their resume and a specific job description. Your task is to provide a high-quality, job-targeted analysis that simulates how a recruiter or Applicant Tracking System (ATS) would assess this resume.

Your output must be a **strictly valid JSON object** with the following fields:

{{
  "matchScore": number,  // integer from 0 to 100 showing how well the resume aligns with the job description,
  "strengths": string[], // specific achievements, skills, or experiences that align strongly with the job,
  "weaknesses": string[], // areas that reduce the effectiveness of the resume, such as unclear impact, lack of detail, or formatting issues,
  "missingSkills": string[], // important skills or requirements from the job description that are not mentioned in the resume,
  "areasForImprovement": string[], // specific, actionable ways to make the resume stronger and better tailored to this job,
  "recruiterPerspective": string, // how a recruiter would likely interpret this resume (e.g. "Seems junior for this role", "Lacks leadership evidence", etc),
  "summary": string // a short paragraph summarizing the overall fit, tone, and quality of the resume for this role
}}

Guidelines:
- Focus on both **technical** and **soft skills**.
- Consider **field-specific expertise** (e.g. data analysis tools, marketing platforms, CAD software, etc. — not just programming).
- Be specific, honest, and constructive — avoid vague or generic feedback.
- Do not return markdown, extra formatting, or any text outside the JSON block.
- Output must be parsable JSON — no trailing commas or comments.

Here is the resume:
{resume}

Here is the job description:
{jd}
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

    data = response.json()

    # now it's a dict, so you can safely index
    raw_output = data["choices"][0]["message"]["content"]
    result = json.loads(raw_output)

    result["fleschReadingEase"] = round(textstat.flesch_reading_ease(resume), 2)
    result["fleschKincaidGrade"] = round(textstat.flesch_kincaid_grade(resume), 2)
    result["tailoringSuggestions"] = suggestion_keyword(get_tailoring_suggestions(resume, jd),jd)

    return result


def gen_cover_letter(resume, jd, applicant_name):
    prompt = f"""
You are a professional career assistant.

Generate a formal, customized **cover letter** based on the applicant's resume and the job description below.

The cover letter must:
- Be in **first person**
- Be concise (max 4 paragraphs)
- Match the **tone of the company and role**
- Be targeted to the **specific job**
- Mention relevant **skills and experiences**
- End with a **professional closing**

Respond with just the **cover letter text** — no explanations, no markdown, and no formatting instructions.

---

Applicant Name: {applicant_name}

Resume:
{resume}

Job Description:
{jd}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)
    print(response.json()["choices"][0]["message"]["content"])
    return response.json()["choices"][0]["message"]["content"]


def suggestion_keyword(keywords, jd):
    prompt = f"""
You are an expert resume consultant. A candidate's resume is missing several key terms that are present in the job description.

Here are the missing keywords:
{", ".join(keywords)}

Job Description:
{jd}

Please generate 3–5 short, natural-sounding suggestions to help the candidate tailor their resume to this job. Each suggestion should explain how or where the candidate might include the missing skills or experience.

Respond with only bullet points.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]



# Load the English model
nlp = spacy.load("en_core_web_sm")

def get_tailoring_suggestions(resume: str, jd: str):
    """
    Suggest what to add or emphasize in the resume based on the job description.
    Returns a list of missing but important keywords from the job description.
    """
    doc_resume = nlp(resume.lower())
    doc_jd = nlp(jd.lower())

    resume_phrases = set([chunk.text.strip() for chunk in doc_resume.noun_chunks])
    jd_phrases = set([chunk.text.strip() for chunk in doc_jd.noun_chunks])

    resume_ents = set([ent.text.strip() for ent in doc_resume.ents])
    jd_ents = set([ent.text.strip() for ent in doc_jd.ents])

    resume_keywords = resume_phrases.union(resume_ents)
    jd_keywords = jd_phrases.union(jd_ents)

    missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords and len(kw) > 3]

    return list(set(missing_keywords))[:10]  # limit to top 10
