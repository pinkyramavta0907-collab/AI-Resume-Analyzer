import os

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from analyzer.resume_parser import extract_resume_text
from analyzer.skill_extractor import extract_skills
from analyzer.job_matcher import calculate_match

from database.database import (
    initialize_database,
    save_analysis,
    get_all_analyses
)


app = Flask(__name__)

app.secret_key = "resume-analyzer-secret-key"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

initialize_database()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        flash("Please upload your resume.")
        return redirect(url_for("home"))

    resume = request.files["resume"]

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if resume.filename == "":
        flash("Please select a resume.")
        return redirect(url_for("home"))

    if not job_description:
        flash("Please enter a job description.")
        return redirect(url_for("home"))

    if not allowed_file(resume.filename):
        flash("Only PDF and DOCX files are supported.")
        return redirect(url_for("home"))

    filename = secure_filename(resume.filename)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(file_path)

    try:

        # Extract text from resume
        resume_text = extract_resume_text(file_path)

        if not resume_text:
            flash("Could not extract text from resume.")
            return redirect(url_for("home"))

        # Extract skills from resume
        resume_skills = extract_skills(resume_text)

        # Compare resume with job description
        result = calculate_match(
            resume_skills,
            job_description
        )

        # Save analysis
        save_analysis(
            filename,
            result["match_percentage"],
            result["matching_skills"],
            result["missing_skills"]
        )

        # Display result
        return render_template(
            "result.html",
            filename=filename,
            resume_skills=resume_skills,
            job_skills=result["job_skills"],
            matching_skills=result["matching_skills"],
            missing_skills=result["missing_skills"],
            match_percentage=result["match_percentage"]
        )

    except Exception as error:

        flash(str(error))
        return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():

    analyses = get_all_analyses()

    return render_template(
        "dashboard.html",
        analyses=analyses
    )


if __name__ == "__main__":
    app.run(debug=True)