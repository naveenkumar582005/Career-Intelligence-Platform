import os

class Config:

    # Flask Secret Key
    SECRET_KEY = "career_intelligence_platform_secret_key"

    # Upload Folder
    UPLOAD_FOLDER = "uploads"

    # Allowed File Types
    ALLOWED_EXTENSIONS = {"pdf"}

    # Maximum Upload Size (10 MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Model Folder
    MODEL_FOLDER = "model"

    # Dataset Folder
    DATASET_FOLDER = "dataset"

    # Jobs Dataset
    JOB_DATASET = os.path.join(
        DATASET_FOLDER,
        "jobs.csv"
    )

    # Model Paths
    PLACEMENT_MODEL = os.path.join(
        MODEL_FOLDER,
        "placement_model.pkl"
    )

    SCALER = os.path.join(
        MODEL_FOLDER,
        "scaler.pkl"
    )

    LABEL_ENCODER = os.path.join(
        MODEL_FOLDER,
        "label_encoder.pkl"
    )

    TFIDF_VECTORIZER = os.path.join(
        MODEL_FOLDER,
        "tfidf_vectorizer.pkl"
    )

    # Resume Upload Path
    RESUME_PATH = os.path.join(
        UPLOAD_FOLDER,
        "resume.pdf"
    )

    # Application Name
    PROJECT_NAME = "Career Intelligence Platform"

    # Version
    VERSION = "1.0.0"

    # Developer
    AUTHOR = "Naveen Kumar"

    DEBUG = True