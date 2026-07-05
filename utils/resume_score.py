class ResumeScoreCalculator:

    def calculate_resume_score(
        self,
        skills_score,
        soft_skills_score,
        internships,
        projects,
        certifications,
        programming_languages,
    ):
        return round(
            skills_score * 0.30
            + soft_skills_score * 0.20
            + internships * 0.15
            + projects * 0.15
            + certifications * 0.10
            + programming_languages * 0.10,
            2,
        )

    def technical_strength(self, skills_score, programming_languages, projects):
        return round(
            skills_score * 0.50 + programming_languages * 0.30 + projects * 0.20,
            2,
        )

    def industry_readiness(self, experience_years, internships, certifications, projects):
        return round(
            experience_years * 0.30
            + internships * 0.30
            + certifications * 0.20
            + projects * 0.20,
            2,
        )

    def career_readiness(self, resume_score, technical_strength, industry_readiness):
        """Weighted average — all inputs are already on a 0-100 scale."""
        score = (
            resume_score * 0.40
            + technical_strength * 0.35
            + industry_readiness * 0.25
        )
        return round(min(score, 100.0), 2)

    def analyze_resume(
        self,
        skills_score,
        soft_skills_score,
        internships,
        projects,
        certifications,
        programming_languages,
        experience_years,
    ):
        resume_score = self.calculate_resume_score(
            skills_score, soft_skills_score, internships, projects, certifications, programming_languages
        )
        technical = self.technical_strength(skills_score, programming_languages, projects)
        industry = self.industry_readiness(experience_years, internships, certifications, projects)
        career = self.career_readiness(resume_score, technical, industry)

        return {
            "resume_score": resume_score,
            "technical_strength": technical,
            "industry_readiness": industry,
            "career_readiness": career,
        }