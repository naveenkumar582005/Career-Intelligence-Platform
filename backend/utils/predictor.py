import numpy as np
import joblib
from utils.logger import logger


class PlacementPredictor:

    FEATURE_ORDER = [
        "cgpa",
        "internships",
        "projects",
        "coding_skills",
        "communication_skills",
        "aptitude_test_score",
        "certifications",
        "backlogs",
    ]

    def __init__(
        self,
        model_path="model/placement_model.pkl",
        scaler_path="model/scaler.pkl",
        encoder_path="model/label_encoder.pkl",
    ):
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
        except Exception as exc:
            logger.exception("Failed to load machine learning models from disk: %s", exc)
            raise exc

    def predict(self, data):
        # Build feature vector in the exact order the model was trained on
        raw = np.array(
            [float(data.get(f, data.get("aptitude_score", 0)) if f == "aptitude_test_score" else float(data[f]))
             for f in self.FEATURE_ORDER],
            dtype=float,
        ).reshape(1, -1)

        scaled = self.scaler.transform(raw)
        pred_idx = int(self.model.predict(scaled)[0])
        proba = self.model.predict_proba(scaled)[0]

        label = self.encoder.inverse_transform([pred_idx])[0]
        confidence = round(float(max(proba)) * 100, 2)

        return {
            "prediction": str(label),
            "confidence": confidence,
            "probability": proba.tolist(),
        }
