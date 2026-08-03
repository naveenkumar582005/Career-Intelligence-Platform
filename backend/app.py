import io
import logging
import os
from datetime import datetime

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import Config
from utils.chart_generator import ChartGenerator
from utils.helper import Helper
from utils.predictor import PlacementPredictor
from utils.resume_parser import ResumeParser
from utils.resume_score import ResumeScoreCalculator
from utils.roadmap import CareerRoadmap
from utils.skill_matcher import SkillMatcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(os.path.join(app.config["STATIC_FOLDER"], "images"), exist_ok=True)

# Fail fast — all models must exist
_required_models = [
    app.config["PLACEMENT_MODEL"],
    app.config["SCALER"],
    app.config["LABEL_ENCODER"],
    app.config["TFIDF_VECTORIZER"],
]
_missing = [p for p in _required_models if not os.path.exists(p)]
if _missing:
    raise FileNotFoundError(
        f"Pre-trained model files not found: {_missing}\n"
        "Please ensure all model files are in backend/model/ folder."
    )

predictor = PlacementPredictor(
    app.config["PLACEMENT_MODEL"],
    app.config["SCALER"],
    app.config["LABEL_ENCODER"],
)
resume_parser = ResumeParser()
resume_calculator = ResumeScoreCalculator()
skill_matcher = SkillMatcher(app.config["JOB_DATASET"], app.config["TFIDF_VECTORIZER"])
roadmap_generator = CareerRoadmap()
helper = Helper()
chart_generator = ChartGenerator(output_dir=os.path.join(app.config["STATIC_FOLDER"], "images"))


def _to_serializable(value):
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_serializable(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def build_analysis_context(form_data, resume_path):
    student_data = {
        "cgpa": float(form_data.get("cgpa", 0)),
        "internships": float(form_data.get("internships", 0)),
        "projects": float(form_data.get("projects", 0)),
        "coding_skills": float(form_data.get("coding_skills", 0)),
        "communication_skills": float(form_data.get("communication_skills", 0)),
        "aptitude_test_score": float(form_data.get("aptitude_score", 0)),
        "certifications": float(form_data.get("certifications", 0)),
        "backlogs": float(form_data.get("backlogs", 0)),
    }

    resume_data = resume_parser.parse_resume(resume_path)
    manual_skills = helper.string_to_skills(form_data.get("skills", ""))
    combined_skills = helper.remove_duplicates(
        manual_skills
        + [s.lower() for s in resume_data.get("skills", [])]
        + resume_data.get("extra_skills", [])
    )

    placement = predictor.predict(student_data)

    skills_score = min(100, len(combined_skills) * 8)
    programming_languages = min(
        100,
        len([s for s in combined_skills if s in {"python", "java", "c", "c++", "javascript", "sql"}]) * 15,
    )

    resume_analysis = resume_calculator.analyze_resume(
        skills_score=skills_score,
        soft_skills_score=float(form_data.get("soft_skills", 0)),
        internships=student_data["internships"] * 20,
        projects=student_data["projects"] * 12,
        certifications=student_data["certifications"] * 15,
        programming_languages=programming_languages,
        experience_years=min(100, student_data["internships"] * 25),
    )

    recommended_jobs = skill_matcher.recommend_jobs(combined_skills, top_n=5)
    target_role = form_data.get("target_role", "")
    best_job = helper.top_role(recommended_jobs) or target_role

    gap = skill_matcher.skill_gap(combined_skills, best_job)
    missing_skills = gap["missing_skills"]
    certifications = skill_matcher.recommended_certifications(best_job)
    roadmap = roadmap_generator.generate_roadmap(missing_skills[:8])

    feature_importance = ChartGenerator.feature_importance_from_input(student_data)
    career_readiness = resume_analysis["career_readiness"]

    # Timestamp string to prevent browser caching of charts
    chart_ts = int(datetime.now().timestamp())
    chart_generator.generate_resume_chart({
        "Resume": resume_analysis["resume_score"],
        "Technical": resume_analysis["technical_strength"],
        "Industry": resume_analysis["industry_readiness"],
        "Career": career_readiness,
    })
    chart_generator.generate_placement_chart(feature_importance)
    chart_generator.generate_shap_summary(feature_importance)

    base_url = "http://localhost:5000"
    return _to_serializable({
        "placement_result": placement["prediction"],
        "placement_probability": placement["confidence"],
        "resume_score": resume_analysis["resume_score"],
        "technical_strength": resume_analysis["technical_strength"],
        "industry_readiness": resume_analysis["industry_readiness"],
        "career_readiness": career_readiness,
        "readiness_level": helper.readiness_level(career_readiness),
        "readiness_message": helper.readiness_message(career_readiness),
        "recommended_jobs": recommended_jobs,
        "missing_skills": missing_skills,
        "certifications": certifications,
        "roadmap": roadmap,
        "resume_email": resume_data.get("email", ""),
        "resume_phone": resume_data.get("phone", ""),
        "parsed_skills": resume_data.get("skills", []),
        "extra_skills": resume_data.get("extra_skills", []),
        "all_skills": combined_skills,
        "target_role": target_role,
        "best_job": best_job,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "charts": {
            "resume_chart": f"{base_url}/static/images/resume_chart.png?v={chart_ts}",
            "placement_chart": f"{base_url}/static/images/placement_chart.png?v={chart_ts}",
            "shap_summary": f"{base_url}/static/images/shap_summary.png?v={chart_ts}",
        }
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "backend operational",
        "service": app.config["PROJECT_NAME"],
        "version": app.config["VERSION"],
        "port": 5000
    })


@app.route("/static/images/<path:filename>", methods=["GET"])
def get_chart(filename):
    return send_from_directory(os.path.join(app.config["STATIC_FOLDER"], "images"), filename)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"status": "error", "message": "Please upload a PDF resume."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected."}), 400

    if not helper.allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Only PDF files are allowed."}), 400

    filename = secure_filename(file.filename)
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(resume_path)

    try:
        results = build_analysis_context(request.form, resume_path)
        return jsonify({"status": "success", "data": results})
    except Exception as exc:
        logger.exception("Analysis failed: %s", exc)
        return jsonify({"status": "error", "message": f"Analysis failed: {str(exc)}"}), 500


@app.route("/api/download-report", methods=["POST"])
def download_report():
    results = request.get_json(silent=True) or {}

    lines = [
        "Career Intelligence Platform - Career Report",
        "=" * 50,
        f"Generated: {results.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M'))}",
        "",
        "Placement Prediction",
        f"- Result: {results.get('placement_result', 'N/A')}",
        f"- Probability: {results.get('placement_probability', 0)}%",
        "",
        "Resume Scores",
        f"- Resume Score: {results.get('resume_score', 0)}",
        f"- Technical Strength: {results.get('technical_strength', 0)}",
        f"- Industry Readiness: {results.get('industry_readiness', 0)}",
        f"- Career Readiness: {results.get('career_readiness', 0)}",
        f"- Level: {results.get('readiness_level', 'N/A')}",
        "",
        f"Best Matching Role: {results.get('best_job', 'N/A')}",
        "",
        "Top Recommended Jobs:",
    ]

    for i, job in enumerate(results.get("recommended_jobs", []), start=1):
        lines.append(f"  {i}. {job.get('job_title')} — {job.get('match_score', 0):.1f}%")

    lines += ["", "Missing Skills:"]
    lines += [f"  - {s}" for s in results.get("missing_skills", [])]

    lines += ["", "Recommended Certifications:"]
    lines += [f"  - {c}" for c in results.get("certifications", [])]

    lines += ["", "Career Roadmap:"]
    for step in results.get("roadmap", []):
        lines.append(f"  - {step.get('skill')}: {step.get('task')} ({step.get('duration')})")

    buf = io.BytesIO("\n".join(lines).encode("utf-8"))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="career_report.txt", mimetype="text/plain")


if __name__ == "__main__":
    print("Starting Career Intelligence Backend REST API on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
