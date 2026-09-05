import re


SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "flask",
    "django",
    "php",
    "sql",
    "mysql",
    "sqlite",
    "mongodb",
    "postgresql",
    "git",
    "github",
    "docker",
    "rest api",
    "machine learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "power bi",
    "excel",
    "linux",
    "networking",
    "cybersecurity",
    "cloud computing",
    "aws",
    "azure"
]


def extract_skills(text):

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    found_skills = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)