import logging
import re

import pdfplumber

logger = logging.getLogger(__name__)

# ── Curated skill vocabulary — O(1) lookup via set ────────────────────────────
_SKILL_SET = {
    # Programming Languages
    "python", "java", "c", "c++", "c#", "r", "go", "golang", "rust", "scala",
    "kotlin", "swift", "typescript", "php", "ruby", "perl", "matlab",

    # Databases
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
    "cassandra", "dynamodb", "oracle", "firebase", "neo4j", "influxdb", "supabase",

    # Web — Frontend
    "html", "css", "javascript", "bootstrap", "tailwind", "react", "angular",
    "vue", "svelte", "next.js", "nuxt.js", "gatsby", "webpack", "vite",

    # Web — Backend
    "node.js", "express", "flask", "django", "fastapi", "spring", "hibernate",
    "asp.net", "laravel", "rails", "graphql", "grpc", "rest api", "json", "xml", "api",

    # AI / ML Frameworks
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "computer vision", "reinforcement learning", "generative ai", "llm",
    "tensorflow", "keras", "pytorch", "scikit-learn", "xgboost", "lightgbm",
    "catboost", "opencv", "hugging face", "transformers", "langchain",
    "llamaindex", "stable diffusion", "ollama", "mlflow", "optuna",

    # Data Engineering / Science
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "scipy",
    "data analysis", "data science", "data engineering", "feature engineering",
    "etl", "apache spark", "hadoop", "kafka", "airflow", "dbt", "pyspark",

    # DevOps / Cloud / Infra
    "git", "github", "gitlab", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "ci/cd", "linux", "bash", "shell scripting",
    "aws", "azure", "gcp", "heroku", "vercel", "netlify", "cloudflare",

    # BI / Analytics
    "power bi", "tableau", "excel", "looker", "metabase", "superset", "grafana",

    # Tools / Platforms
    "jira", "confluence", "figma", "postman", "swagger", "jupyter",
    "streamlit", "gradio", "vs code",

    # Soft Skills / Methodologies
    "problem solving", "communication", "leadership", "teamwork",
    "agile", "scrum", "kanban",
}

# ── Stopword list for heuristic fallback ──────────────────────────────────────
_STOPWORDS = {
    "the", "and", "for", "with", "from", "have", "has", "had", "are", "was",
    "were", "that", "this", "will", "can", "use", "used", "using", "such",
    "also", "more", "very", "been", "being", "about", "into", "over", "than",
    "then", "when", "where", "which", "while", "their", "they", "them", "these",
    "those", "both", "each", "any", "all", "some", "our", "you", "your", "my",
    "his", "her", "its", "we", "he", "she", "it", "in", "of", "to", "a", "an",
    "is", "at", "by", "on", "or", "as", "if", "be", "do", "did", "not", "but",
    "work", "worked", "working", "experience", "project", "projects",
    "university", "college", "school", "degree", "bachelor", "master",
    "engineer", "developer", "student", "intern", "internship", "company",
    "team", "member", "strong", "good", "excellent", "ability", "skills",
    "knowledge", "proficient", "familiar", "learning", "implement",
    "developed", "designed", "built", "created", "managed", "led",
    "responsible", "including", "during", "through", "based", "related",
    "various", "multiple", "different", "following", "between", "within",
    "programming", "language", "technologies", "tools", "frameworks",
}

# ── Regex to find the Skills section in a resume ─────────────────────────────
_SKILLS_SECTION_RE = re.compile(
    r"(?:technical\s+skills?|core\s+competenc(?:ies|y)|skills?\s*[&:]\s*(?:abilities|expertise|technologies)?"
    r"|key\s+skills?|tools?\s*[&:]\s*technologies?|competenc(?:ies|y)|areas?\s+of\s+expertise)"
    r"[:\s]*\n(.*?)(?=\n[A-Z][A-Z\s]{3,}\n|\Z)",
    re.IGNORECASE | re.DOTALL,
)


class ResumeParser:

    def extract_text(self, pdf_path):
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as exc:
            logger.warning("PDF read error for %s: %s", pdf_path, exc)
        return text

    def _clean(self, text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9+#.\s/]", " ", text)
        return re.sub(r"\s+", " ", text)

    def extract_known_skills(self, text):
        """Match text against the curated _SKILL_SET vocabulary (O(1) per skill)."""
        cleaned = self._clean(text)
        return sorted(skill for skill in _SKILL_SET if skill in cleaned)

    def extract_unknown_skills(self, raw_text):
        """
        Heuristic fallback: locate the Skills section and extract tokens
        that are NOT already in _SKILL_SET.
        Useful for catching modern/niche tools like FastAPI, LangChain, etc.
        """
        # Try to isolate the skills section first; fall back to full text
        match = _SKILLS_SECTION_RE.search(raw_text)
        section = match.group(1) if match else raw_text

        # Split on common delimiters used in skill lists
        tokens = re.split(r"[,|\n•\-–/]", section)
        extras = set()
        for tok in tokens:
            tok = tok.strip().lower()
            tok = re.sub(r"\s+", " ", tok)
            # Accept tokens that are 2–35 chars, contain a letter,
            # are not pure digits, and not in stopwords or known vocab
            if (
                2 <= len(tok) <= 35
                and not tok.isdigit()
                and tok not in _STOPWORDS
                and tok not in _SKILL_SET
                and re.search(r"[a-zA-Z]", tok)
            ):
                extras.add(tok)
        return sorted(extras)

    def extract_email(self, text):
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return match.group(0) if match else ""

    def extract_phone(self, text):
        match = re.search(r"\+?\d[\d\s-]{8,15}", text)
        return match.group(0) if match else ""

    def parse_resume(self, pdf_path):
        text = self.extract_text(pdf_path)
        known_skills = self.extract_known_skills(text)
        extra_skills = self.extract_unknown_skills(text)
        return {
            "text": text,
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": known_skills,          # matched against vocabulary
            "extra_skills": extra_skills,    # detected from resume sections (heuristic)
        }