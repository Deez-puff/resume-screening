# ── Data Science / IT Skills List ────────────────────────
SKILLS = [
    # Programming Languages
    "python", "r", "java", "scala", "c++", "javascript",

    # Data & Databases
    "sql", "mysql", "postgresql", "mongodb", "hadoop", "spark",

    # Machine Learning & AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "neural network", "reinforcement learning",

    # ML Libraries & Frameworks
    "scikit-learn", "tensorflow", "keras", "pytorch", "xgboost",
    "pandas", "numpy", "matplotlib", "seaborn",

    # Cloud & Tools
    "aws", "azure", "google cloud", "docker", "kubernetes", "git",
    "jenkins", "airflow",

    # Data Skills
    "data analysis", "data visualization", "data wrangling",
    "feature engineering", "statistical analysis", "data mining",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving",
    "project management", "agile"
]

def extract_skills(text):
    """
    Scans cleaned resume text and returns
    a list of matching skills found
    """
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills