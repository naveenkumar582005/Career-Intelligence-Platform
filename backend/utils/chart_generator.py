import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


class ChartGenerator:

    def __init__(self, output_dir="static/images"):

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_resume_chart(self, scores, filename="resume_chart.png"):

        labels = list(scores.keys())
        values = list(scores.values())

        plt.figure(figsize=(8, 5))
        colors = ["#16a34a", "#f59e0b", "#0891b2", "#dc2626"]
        plt.bar(labels, values, color=colors[: len(labels)])
        plt.ylim(0, 100)
        plt.title("Resume Analytics")
        plt.ylabel("Score")
        plt.tight_layout()

        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=120)
        plt.close()

        return path

    def generate_placement_chart(self, feature_importance, filename="placement_chart.png"):

        labels = list(feature_importance.keys())
        values = list(feature_importance.values())

        plt.figure(figsize=(8, 5))
        plt.barh(labels, values, color="#2563eb")
        plt.title("Placement Feature Contribution")
        plt.xlabel("Relative Impact")
        plt.tight_layout()

        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=120)
        plt.close()

        return path

    def generate_shap_summary(self, feature_importance, filename="shap_summary.png"):

        labels = list(feature_importance.keys())
        values = list(feature_importance.values())

        plt.figure(figsize=(9, 5))
        sorted_pairs = sorted(zip(values, labels), reverse=True)
        values, labels = zip(*sorted_pairs)

        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(labels)))
        plt.barh(labels, values, color=colors)
        plt.title("Explainable AI - Feature Contribution (SHAP-style)")
        plt.xlabel("Impact Score")
        plt.tight_layout()

        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=120)
        plt.close()

        return path

    @staticmethod
    def feature_importance_from_input(data):

        return {
            "CGPA": float(data["cgpa"]) * 10,
            "Internships": float(data["internships"]) * 15,
            "Projects": float(data["projects"]) * 8,
            "Coding Skills": float(data["coding_skills"]) * 0.6,
            "Communication": float(data["communication_skills"]) * 0.4,
            "Aptitude": float(data.get("aptitude_test_score", data.get("aptitude_score", 0))) * 0.4,
            "Certifications": float(data["certifications"]) * 12,
            "Backlogs": max(0, 100 - float(data["backlogs"]) * 20)
        }
