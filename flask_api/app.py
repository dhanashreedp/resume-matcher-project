from flask import Flask, request, jsonify
import spacy
from PyPDF2 import PdfReader
from matcher import match_jobs
import string
from spacy.lang.en.stop_words import STOP_WORDS
import fitz 

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_skills(doc):
    words = [token.text.lower().strip(string.punctuation)
             for token in doc if token.is_alpha and not token.is_stop]
    
    known_skills = {"python", "django", "flask", "sql", "aws", "pandas", "numpy", "machine learning", "nlp"}

    # Match known skills found in resume
    matched_skills = list(set(words) & known_skills)
    return matched_skills

def extract_text_from_pdf(file_storage):
    text = ""
    with fitz.open(stream=file_storage.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route("/parse_and_match", methods=["POST"])
def parse_and_match():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files["resume"]
    resume_text = extract_text_from_pdf(file)
    doc = nlp(resume_text)

    skills = extract_skills(doc)

    candidate_info = {
        "name": doc.ents[0].text if doc.ents else "Unknown",
        "skills": skills
    }

    matched_jobs = match_jobs(skills)

    return jsonify({
        "candidate_info": candidate_info,
        "matched_jobs": matched_jobs
    })

if __name__ == "__main__":
    app.run(debug=True)
