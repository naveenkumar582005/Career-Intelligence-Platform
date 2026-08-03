import os
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    print("Starting Career Intelligence Frontend Server on http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=True)
