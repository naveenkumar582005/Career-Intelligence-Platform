import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class SkillMatcher:

    def __init__(self, jobs_path="dataset/jobs.csv", vectorizer_path="model/tfidf_vectorizer.pkl"):
        self.jobs = pd.read_csv(jobs_path)
        # Normalize column names once at load time
        self.jobs.columns = [c.strip().lower().replace(" ", "_") for c in self.jobs.columns]
        self.jobs["skills"] = self.jobs["skills"].fillna("")

        self.vectorizer = joblib.load(vectorizer_path)
        # Pre-compute job vectors at startup for faster repeated queries
        self.job_vectors = self.vectorizer.transform(self.jobs["skills"])

    def recommend_jobs(self, student_skills, top_n=5):
        skill_str = ", ".join(student_skills) if isinstance(student_skills, list) else student_skills
        student_vector = self.vectorizer.transform([skill_str])
        similarity = cosine_similarity(student_vector, self.job_vectors)[0]

        df = self.jobs.copy()
        df["match_score"] = similarity * 100
        top = df.nlargest(top_n, "match_score")
        return top.to_dict(orient="records")

    def get_required_skills(self, job_title):
        row = self.jobs[self.jobs["job_title"].str.lower() == job_title.lower()]
        if row.empty:
            return []
        return [s.strip().lower() for s in row.iloc[0]["skills"].split(",") if s.strip()]

    def skill_gap(self, student_skills, job_title):
        if isinstance(student_skills, str):
            student_skills = [s.strip().lower() for s in student_skills.split(",") if s.strip()]
        else:
            student_skills = [s.strip().lower() for s in student_skills]

        required = self.get_required_skills(job_title)
        matched, missing = [], []
        for skill in required:
            if any(skill in ss or ss in skill for ss in student_skills):
                matched.append(skill)
            else:
                missing.append(skill)
        return {"matched_skills": matched, "missing_skills": missing}

    def recommended_certifications(self, job_title):
        row = self.jobs[self.jobs["job_title"].str.lower() == job_title.lower()]
        if row.empty:
            return []
        certs = row.iloc[0].get("certifications", "")
        if pd.isna(certs):
            return []
        return [c.strip() for c in str(certs).split(",") if c.strip()]
