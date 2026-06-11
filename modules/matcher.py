import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# SKILLS DATABASE

SKILLS = [

    "python",
    "java",
    "c++",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "artificial intelligence",
    "data analysis",
    "git",
    "github",
    "communication",
    "leadership",
    "problem solving",
    "node.js",
    "express.js",
    "firebase",
    "tailwind",
    "bootstrap",
    "api",
    "rest api",
    "deep learning",
    "data science",
    "figma",
    "ui ux",
    "android",
    "kotlin"

]

# CLEAN TEXT


def clean_text(text):

    text = text.lower()

    # REMOVE SPECIAL SYMBOLS

    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)

    # REMOVE EXTRA SPACES

    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# EXTRACT SKILLS


def extract_skills(text):

    text = clean_text(text)

    detected_skills = []

    # SKILL ALIASES

    skill_aliases = {

        "python": ["python", "py"],

        "java": ["java"],

        "c++": ["c++", "cpp"],

        "html": ["html"],

        "css": ["css"],

        "javascript": ["javascript", "js"],

        "react": ["react", "reactjs", "react.js"],

        "node.js": ["node", "nodejs", "node.js"],

        "express.js": ["express", "expressjs"],

        "flask": ["flask"],

        "django": ["django"],

        "sql": ["sql", "mysql"],

        "mongodb": ["mongodb", "mongo"],

        "firebase": ["firebase"],

        "tailwind": ["tailwind"],

        "bootstrap": ["bootstrap"],

        "machine learning": [
            "machine learning",
            "ml"
        ],

        "deep learning": [
            "deep learning"
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "ai"
        ],

        "data science": [
            "data science"
        ],

        "data analysis": [
            "data analysis",
            "data analytics"
        ],

        "git": ["git"],

        "github": ["github"],

        "api": ["api"],

        "rest api": ["rest api"],

        "figma": ["figma"],

        "ui ux": ["ui ux", "ui/ux"],

        "android": ["android"],

        "kotlin": ["kotlin"],

        "communication": ["communication"],

        "leadership": ["leadership"],

        "problem solving": [
            "problem solving",
            "problem-solving"
        ]

    }

    for main_skill, aliases in skill_aliases.items():

        for alias in aliases:

            if alias.lower() in text:

                detected_skills.append(main_skill)
                break

    return list(set(detected_skills))

# MATCH SCORE


def calculate_match(resume_text, job_description):

    resume_text = clean_text(resume_text)

    job_description = clean_text(job_description)

    # COSINE SIMILARITY

    documents = [resume_text, job_description]

    vectorizer = CountVectorizer()

    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    similarity_score = similarity * 60

    # SKILL MATCH BONUS

    matched_skills = get_matched_skills(
        resume_text,
        job_description
    )

    job_skills = extract_skills(job_description)

    skill_score = 0

    if len(job_skills) > 0:

        skill_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 40

    final_score = similarity_score + skill_score

    if final_score > 100:
        final_score = 100

    return round(final_score, 2)

# FIND MISSING SKILLS


def get_missing_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    missing_skills = []

    for skill in job_skills:

        if skill not in resume_skills:

            missing_skills.append(skill)

    return list(set(missing_skills))

# MATCHED SKILLS


def get_matched_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    matched_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matched_skills.append(skill)

    return list(set(matched_skills))

# GENERATE RESUME SUMMARY


def generate_resume_summary(resume_text):

    skills = extract_skills(resume_text)

    summary = ""

    if skills:

        summary += "Candidate Skills:\n\n"

        for skill in skills:

            summary += f"• {skill.title()}\n"

    else:

        summary += "No major technical skills detected."

    return summary

# ATS SCORE CALCULATION


def calculate_ats_score(
    resume_text,
    job_description
):

    score = 0

    resume_text = clean_text(resume_text)

    job_description = clean_text(job_description)

    # MATCHED SKILLS

    matched_skills = get_matched_skills(
        resume_text,
        job_description
    )

    job_skills = extract_skills(
        job_description
    )

    # SKILL SCORE

    if job_skills:

        skill_percentage = (
            len(matched_skills)
            / len(job_skills)
        ) * 45

        score += skill_percentage

    # WORD COUNT

    word_count = len(resume_text.split())

    if word_count >= 450:

        score += 15

    elif word_count >= 250:

        score += 10

    # EMAIL

    if "@" in resume_text:
        score += 10

    # PHONE

    phone_pattern = r'\d{10}'

    if re.search(phone_pattern, resume_text):
        score += 10

    # LINKEDIN

    if "linkedin" in resume_text:
        score += 5

    # GITHUB

    if "github" in resume_text:
        score += 5

    # PROJECT SECTION

    if "project" in resume_text:
        score += 5

    # EXPERIENCE SECTION

    if "experience" in resume_text:
        score += 5

    # EDUCATION

    education_keywords = [
        "btech",
        "bca",
        "mca",
        "degree",
        "university",
        "college"
    ]

    if any(word in resume_text for word in education_keywords):

        score += 5

    # CERTIFICATIONS

    if "certification" in resume_text:
        score += 5

    # LIMIT SCORE

    if score > 100:
        score = 100

    return round(score)

# GENERATE IMPROVEMENT SUGGESTIONS


def generate_resume_feedback(

    score,
    missing_skills,
    resume_text

):

    feedback = []

    resume_text = resume_text.lower()

    # SCORE ANALYSIS

    if score < 50:

        feedback.append(
            "Your resume has a low match score. Add more relevant technical skills and job-specific keywords."
        )

    elif score < 75:

        feedback.append(
            "Your resume is moderately optimized. Improve project descriptions and technical depth."
        )

    else:

        feedback.append(
            "Your resume is strongly aligned with the job description."
        )

    # MISSING SKILLS

    if missing_skills:

        feedback.append(
            "Consider adding these important skills: " +
            ", ".join(missing_skills[:5])
        )

    # GITHUB

    if "github" not in resume_text:

        feedback.append(
            "Add your GitHub profile to improve technical credibility."
        )

    # LINKEDIN

    if "linkedin" not in resume_text:

        feedback.append(
            "Include your LinkedIn profile for professional visibility."
        )

    # PROJECTS

    if "project" not in resume_text:

        feedback.append(
            "Add project experience to showcase practical implementation skills."
        )

    # EXPERIENCE

    if "experience" not in resume_text:

        feedback.append(
            "Mention internships, freelance work, or real-world experience."
        )

    # ACTION VERBS

    achievement_words = [
        "improved",
        "developed",
        "designed",
        "created",
        "built",
        "implemented"
    ]

    if not any(word in resume_text for word in achievement_words):

        feedback.append(
            "Use strong action verbs like Developed, Built, Designed, or Implemented."
        )

    # RESUME LENGTH

    if len(resume_text.split()) < 200:

        feedback.append(
            "Your resume is too short. Add more technical details and achievements."
        )

    return feedback
