from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from modules.matcher import (
    calculate_match,
    get_missing_skills,
    get_matched_skills,
    generate_resume_summary,
    calculate_ats_score,
    generate_resume_feedback
)

from modules.resume_parser import (
    extract_pdf_text,
    extract_docx_text,
    extract_resume_sections
)

import os


app = Flask(__name__)

# SECRET KEY

app.secret_key = "resume_analyzer_secret"

# DATABASE CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# USER MODEL


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

# ANALYSIS MODEL


class Analysis(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    filename = db.Column(db.String(200))

    match_score = db.Column(db.Float)

    ats_score = db.Column(db.Float)

    missing_skills = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

# CREATE DATABASE


with app.app_context():
    db.create_all()

# LOGIN ROUTE


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session["user_id"] = user.id
            session["user_name"] = user.fullname

            return redirect("/dashboard")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# SIGNUP ROUTE


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already exists"

        new_user = User(
            fullname=fullname,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    return render_template("signup.html")

# DASHBOARD ROUTE


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )

# HISTORY ROUTE


@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/")

    analyses = Analysis.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Analysis.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        analyses=analyses
    )

# ANALYZE ROUTE


# ANALYZE ROUTE

@app.route("/analyze", methods=["POST"])
def analyze():

    # CHECK LOGIN

    if "user_id" not in session:
        return redirect("/")

    # GET FORM DATA

    resume = request.files["resume"]

    job_description = request.form["job_description"]

    # CREATE UPLOAD FOLDER

    upload_folder = "static/uploads"

    os.makedirs(upload_folder, exist_ok=True)

    # SAVE FILE

    upload_path = os.path.join(
        upload_folder,
        resume.filename
    )

    resume.save(upload_path)

    # EXTRACT RESUME TEXT

    extracted_text = ""

    if resume.filename.endswith(".pdf"):

        extracted_text = extract_pdf_text(upload_path)

    elif resume.filename.endswith(".docx"):

        extracted_text = extract_docx_text(upload_path)

    # PARSE RESUME DATA

    parsed_data = extract_resume_sections(
        extracted_text
    )

    # CALCULATE MATCH SCORE

    score = calculate_match(
        extracted_text,
        job_description
    )

    # FIND MISSING SKILLS

    missing_skills = get_missing_skills(
        extracted_text,
        job_description
    )

    # FIND MATCHED SKILLS

    matched_skills = get_matched_skills(
        extracted_text,
        job_description
    )

    # DEBUG

    print("MATCHED:", matched_skills)
    print("MISSING:", missing_skills)

    # GENERATE RESUME SUMMARY

    resume_summary = generate_resume_summary(
        extracted_text
    )

    # CALCULATE ATS SCORE

    ats_score = calculate_ats_score(
        extracted_text,
        job_description
    )

    # GENERATE FEEDBACK

    feedback = generate_resume_feedback(
        score,
        missing_skills,
        extracted_text
    )

    # SAVE ANALYSIS

    new_analysis = Analysis(

        user_id=session["user_id"],

        filename=resume.filename,

        match_score=score,

        ats_score=ats_score,

        missing_skills=", ".join(missing_skills)

    )

    db.session.add(new_analysis)

    db.session.commit()

    # RENDER RESULT PAGE

    return render_template(

        "result.html",

        score=score,

        ats_score=ats_score,

        matched_skills=matched_skills,

        total_missing=len(missing_skills),

        missing_skills=missing_skills,

        feedback=feedback,

        extracted_text=extracted_text,

        resume_summary=resume_summary,

        job_description=job_description,

        parsed_data=parsed_data

    )

# LOGOUT ROUTE


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# RUN APPLICATION


if __name__ == "__main__":
    app.run(debug=True)
