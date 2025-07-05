import requests

def match_jobs(candidate_skills):
    try:
        response = requests.get("http://localhost:8000/api/jobs/")
        response.raise_for_status()
        jobs = response.json()
    except Exception as e:
        return [{"error": "Could not fetch jobs", "details": str(e)}]

    matched = []
    for job in jobs:
        job_skills = [skill.strip().lower() for skill in job["skills_required"].split(",")]
        matched_skills = list(set(job_skills) & set(map(str.lower, candidate_skills)))
        if matched_skills:
            matched.append({
                "job_title": job["title"],
                "matched_skills": matched_skills
            })
    return matched
