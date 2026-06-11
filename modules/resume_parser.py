import PyPDF2
import docx
import re

# CLEAN TEXT FUNCTION


def clean_resume_text(text):

    # KEEP LINE BREAKS

    text = text.replace("\t", " ")

    # REMOVE EXTRA SPACES

    text = re.sub(r' +', ' ', text)

    # CLEAN SPECIAL SYMBOLS

    text = re.sub(r'[^\w\s@.+#:/()\-•]', ' ', text)

    # REMOVE MULTIPLE NEWLINES

    text = re.sub(r'\n+', '\n', text)

    return text.strip()

# PDF TEXT EXTRACTION


def extract_pdf_text(file_path):

    text = ""

    with open(file_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return clean_resume_text(text)

# DOCX TEXT EXTRACTION


def extract_docx_text(file_path):

    doc = docx.Document(file_path)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return clean_resume_text(text)

# STRUCTURED RESUME PARSER


def extract_resume_sections(text):

    data = {

        "name": "",

        "email": "",

        "phone": "",

        "linkedin": "",

        "skills": [],

        "education": [],

        "experience": [],

        "projects": [],

        "certifications": []

    }

    clean_text = text.lower()

    # =========================
    # EMAIL EXTRACTION
    # =========================

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email:

        data["email"] = email[0]

    # =========================
    # PHONE EXTRACTION
    # =========================

    phone = re.findall(
        r"(?:\+91[-\s]?)?[6-9]\d{9}",
        text
    )

    if phone:

        data["phone"] = phone[0]

    # =========================
    # LINKEDIN EXTRACTION
    # =========================

    linkedin = re.findall(
        r"(https?:\/\/)?(www\.)?linkedin\.com\/[A-Za-z0-9\/\-_%]+",
        text
    )

    if linkedin:

        data["linkedin"] = "LinkedIn Profile Found"

    # =========================
    # NAME EXTRACTION
    # =========================

    lines = text.split("\n")

    possible_names = []

    for line in lines[:10]:

        line = line.strip()

        words = line.split()

        if (

            len(words) >= 2 and
            len(words) <= 4 and
            all(word[0].isupper() for word in words if word[0].isalpha()) and
            "resume" not in line.lower() and
            "curriculum" not in line.lower() and
            "vitae" not in line.lower() and
            "email" not in line.lower()

        ):

            possible_names.append(line)

    if possible_names:

        data["name"] = possible_names[0]

    # =========================
    # SKILLS DATABASE
    # =========================

    skills_db = [

        "python",
        "java",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "next.js",
        "vue",
        "angular",
        "node.js",
        "express.js",
        "flask",
        "django",
        "sql",
        "mysql",
        "mongodb",
        "firebase",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "data analysis",
        "numpy",
        "pandas",
        "tensorflow",
        "pytorch",
        "opencv",
        "git",
        "github",
        "bootstrap",
        "tailwind",
        "android",
        "kotlin",
        "figma",
        "api",
        "rest api",
        "aws",
        "docker",
        "kubernetes",
        "power bi",
        "excel"

    ]

    found_skills = []

    for skill in skills_db:

        if skill.lower() in clean_text:

            found_skills.append(skill)

    data["skills"] = sorted(list(set(found_skills)))

    # =========================
    # EDUCATION KEYWORDS
    # =========================

    education_keywords = [

        "bca",
        "mca",
        "btech",
        "be",
        "b.e",
        "bsc",
        "msc",
        "computer science",
        "information technology",
        "cgpa",
        "university",
        "college",
        "school",
        "education",
        "master",
        "bachelor"

    ]

    # =========================
    # EXPERIENCE KEYWORDS
    # =========================

    experience_keywords = [

        "intern",
        "internship",
        "developer",
        "experience",
        "worked",
        "company",
        "software engineer",
        "frontend developer",
        "backend developer",
        "web developer",
        "full stack"

    ]

    # =========================
    # PROJECT KEYWORDS
    # =========================

    project_keywords = [

        "project",
        "developed",
        "built",
        "created",
        "designed",
        "implemented",
        "application",
        "website",
        "system",
        "platform",
        "dashboard"

    ]

    # =========================
    # CERTIFICATION KEYWORDS
    # =========================

    certification_keywords = [

        "certification",
        "certificate",
        "course",
        "udemy",
        "coursera",
        "nptel"

    ]

    # =========================
    # SPLIT INTO LINES
    # =========================

    lines = text.split("\n")

    for line in lines:

        sentence = line.strip()

        lower_sentence = sentence.lower()

        if len(sentence) < 5:

            continue

        # EDUCATION

        if any(word in lower_sentence for word in education_keywords):

            data["education"].append(sentence)

        # EXPERIENCE

        if any(word in lower_sentence for word in experience_keywords):

            data["experience"].append(sentence)

        # PROJECTS

        if any(word in lower_sentence for word in project_keywords):

            data["projects"].append(sentence)

        # CERTIFICATIONS

        if any(word in lower_sentence for word in certification_keywords):

            data["certifications"].append(sentence)

    # =========================
    # REMOVE DUPLICATES
    # =========================

    data["education"] = list(set(data["education"]))

    data["experience"] = list(set(data["experience"]))

    data["projects"] = list(set(data["projects"]))

    data["certifications"] = list(set(data["certifications"]))

    return data
