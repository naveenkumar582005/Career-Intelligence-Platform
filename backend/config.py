import os

class Config:
    # Flask Secret Key
    SECRET_KEY = "career_intelligence_platform_secret_key"

    # Base Directory for backend
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Upload Folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Allowed File Types
    ALLOWED_EXTENSIONS = {"pdf"}

    # Maximum Upload Size (10 MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Model Folder
    MODEL_FOLDER = os.path.join(BASE_DIR, "model")

    # Dataset Folder
    DATASET_FOLDER = os.path.join(BASE_DIR, "dataset")

    # Static Folder for generated charts
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")

    # Jobs Dataset
    JOB_DATASET = os.path.join(DATASET_FOLDER, "jobs.csv")

    # Model Paths
    PLACEMENT_MODEL = os.path.join(MODEL_FOLDER, "placement_model.pkl")
    SCALER = os.path.join(MODEL_FOLDER, "scaler.pkl")
    LABEL_ENCODER = os.path.join(MODEL_FOLDER, "label_encoder.pkl")
    TFIDF_VECTORIZER = os.path.join(MODEL_FOLDER, "tfidf_vectorizer.pkl")

    # Resume Upload Path
    RESUME_PATH = os.path.join(UPLOAD_FOLDER, "resume.pdf")

    # Application Metadata
    PROJECT_NAME = "Career Intelligence Platform API"
    VERSION = "1.0.0"
    AUTHOR = "Naveen Kumar"

    DEBUG = True
