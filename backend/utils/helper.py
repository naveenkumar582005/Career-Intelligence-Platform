import os
import re


class Helper:

    @staticmethod
    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"

    @staticmethod
    def string_to_skills(skill_string):
        if not skill_string:
            return []
        return [s.strip().lower() for s in skill_string.split(",") if s.strip()]

    @staticmethod
    def remove_duplicates(skills):
        return sorted(set(skills))

    @staticmethod
    def top_role(recommended_jobs):
        return recommended_jobs[0]["job_title"] if recommended_jobs else None

    @staticmethod
    def readiness_level(score):
        if score >= 85:
            return "Excellent"
        if score >= 70:
            return "Good"
        if score >= 50:
            return "Average"
        return "Needs Improvement"

    @staticmethod
    def readiness_message(score):
        if score >= 85:
            return "You are highly prepared for placements."
        if score >= 70:
            return "Your profile is good. Improve a few skills."
        if score >= 50:
            return "Strengthen technical and practical skills."
        return "Significant improvement is required before placements."