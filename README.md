# 📄 Resume Screening & Ranking System

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn)
![NLTK](https://img.shields.io/badge/NLTK-NLP-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit)
![GitHub](https://img.shields.io/badge/GitHub-Public-black?style=for-the-badge&logo=github)

> An ML-powered Resume Screening & Ranking System that automatically screens, scores, and ranks candidates based on a job description using Natural Language Processing (NLP) techniques.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Web App Usage](#web-app-usage)
- [How Candidates Are Scored](#how-candidates-are-scored)
- [Why Certain Candidates Rank Higher](#why-certain-candidates-rank-higher)
- [Skill Gap Identification](#skill-gap-identification)
- [Dataset](#dataset)
- [Future Improvements](#future-improvements)

---

## 🧠 About the Project

Hiring teams receive hundreds of resumes for a single job role. Manually reviewing every resume is time-consuming, inconsistent, and error-prone.

This project solves that problem by building a **Machine Learning-based Resume Screening & Ranking System** that:

- Automatically reads and cleans resume text
- Extracts relevant skills from each resume
- Compares resumes against a job description
- Scores and ranks candidates based on role fit
- Highlights missing or required skills
- Displays results in an interactive web application

This workflow closely mirrors modern HR-tech and Applicant Tracking Systems (ATS) used in real-world recruitment platforms.

---

## ⚙️ How It Works

```text
Resume Dataset (CSV)
        │
        ▼
┌─────────────────────┐
│  Text Cleaning      │
│ (preprocessor.py)   │
│ Lowercase, remove   │
│ symbols, stopwords, │
│ lemmatization       │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Skill Extraction    │
│(skill_extractor.py) │
│ Match against 40+   │
│ IT & DS skills      │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ TF-IDF Vectorizer   │
│    (scorer.py)      │
│ Convert text into   │
│ numerical vectors   │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Cosine Similarity   │
│    (scorer.py)      │
│ Compute JD-resume   │
│ similarity score    │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Ranking & Skill Gap │
│    (ranker.py)      │
│ Rank candidates and │
│ identify gaps       │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Results Display     │
│      (app.py)       │
│ Tables, Charts,     │
│ Heatmaps            │
└─────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|----------|-------------|
| 📂 Upload Any Dataset | Accepts any CSV file containing resume text |
| 🧹 Text Cleaning | Removes noise, punctuation, stopwords, and performs lemmatization |
| 🔍 Skill Extraction | Detects 40+ Data Science and IT skills |
| 🤖 ML Scoring | Uses TF-IDF and Cosine Similarity |
| 🏅 Candidate Ranking | Orders candidates from best to worst match |
| 🟩🟥 Skill Gap Analysis | Displays matched and missing skills |
| 📊 Score Visualization | Bar chart comparison of top candidates |
| 🗺️ Skill Heatmap | Visual representation of skill coverage |
| 🌐 Streamlit Web App | Interactive browser-based interface |
| ⚙️ Configurable | Choose text column and filter categories |

---

## 📁 Project Structure

```text
resume-screening/
│
├── data/
│   └── Resume.csv
│
├── src/
│   ├── __init__.py
│   ├── preprocessor.py
│   ├── skill_extractor.py
│   ├── scorer.py
│   └── ranker.py
│
├── app.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|-----------|--------|
| Programming Language | Python 3.14 |
| NLP | NLTK |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Web Framework | Streamlit |
| Version Control | Git & GitHub |

---

## 📦 Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Deez-puff/resume-screening.git
cd resume-screening
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model

```bash
python -m spacy download en_core_web_md
```

### 4. Download the Dataset

Download the dataset from Kaggle:

https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

Place the downloaded file inside the `data/` folder:

```text
resume-screening/
└── data/
    └── Resume.csv
```

---

## ▶️ How to Run

### Option 1 — Streamlit Web App (Recommended)

```bash
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

### Option 2 — Terminal Mode

```bash
python main.py
```

Outputs rankings directly in the terminal and saves visualizations.

---

## 🌐 Web App Usage

1. Upload a CSV file containing resumes
2. Select the column that contains resume text
3. Choose a job category (optional)
4. Enter a job description
5. Click **Screen and Rank Resumes**
6. Review the results:
   - 📋 Ranked candidate table
   - 📊 Candidate score chart
   - 🗺️ Skill heatmap
   - 🔍 Detailed skill gap analysis

---

## 📐 How Candidates Are Scored

### Step 1 — TF-IDF Vectorization

Each resume and the job description are converted into numerical vectors.

**TF (Term Frequency)**

Measures how frequently a word appears in a resume.

**IDF (Inverse Document Frequency)**

Measures how unique a word is across all resumes.

Words that are important and distinctive receive higher weights.

### Step 2 — Cosine Similarity

The similarity between each resume vector and the job description vector is computed.

| Score | Interpretation |
|---------|---------------|
| 1.00 | Perfect Match |
| 0.75 | Strong Match |
| 0.50 | Moderate Match |
| 0.25 | Weak Match |
| 0.00 | No Match |

---

## 🏅 Why Certain Candidates Rank Higher

Candidates receive higher rankings when they:

1. Include more keywords from the job description
2. Possess more required technical skills
3. Mention relevant experience and technologies
4. Use specific industry terminology
5. Demonstrate stronger alignment with the role requirements

---

## 🔍 Skill Gap Identification

For every candidate:

```text
Required Skills  = Skills extracted from Job Description

Candidate Skills = Skills extracted from Resume

Matched Skills   = Required Skills ∩ Candidate Skills

Missing Skills   = Required Skills - Candidate Skills
```

### Visual Indicators

- 🟩 Green = Skill Present
- 🟥 Red = Skill Missing

This helps recruiters quickly identify strengths and weaknesses for each candidate.

---

## 📊 Dataset

### Kaggle Resume Dataset

- 2,484 resumes
- 24 job categories
- Includes IT, HR, Finance, Healthcare, Engineering, and more

Dataset Link:

https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

> Note: The dataset is not included in this repository because of its size. Please download it separately and place it inside the `data/` directory.

---

## 🚀 Future Improvements

- [ ] PDF Resume Upload Support
- [ ] Advanced Skill Extraction using spaCy NER
- [ ] Weighted Skill Scoring
- [ ] Multiple Job Description Comparison
- [ ] Export Results to Excel/PDF
- [ ] Streamlit Cloud Deployment
- [ ] Resume Summarization using Transformer Models
- [ ] Semantic Matching with Sentence Transformers
- [ ] ATS Compatibility Score
- [ ] Recruiter Dashboard Analytics

---

## 👨‍💻 Author

**Deepak Rajesh**

Built as part of **Future Interns ML Task 3 — 2026**

---

## 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project for educational and professional purposes.
