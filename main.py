# ============================================================
# Resume Screening & Ranking System
# ML Task 3 — Future Interns 2026
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('src')

from preprocessor import clean_text
from skill_extractor import extract_skills
from scorer import score_resumes
from ranker import rank_candidates

# ── 1. Load Dataset ───────────────────────────────────────
print("=" * 50)
print("   RESUME SCREENING & RANKING SYSTEM")
print("=" * 50)

df = pd.read_csv("data/Resume.csv")
ds_resumes = df[df['Category'] == 'INFORMATION-TECHNOLOGY'].reset_index(drop=True)
print(f"\n✅ Resumes loaded: {len(ds_resumes)}")

# ── 2. Clean Resumes ──────────────────────────────────────
print("\n⏳ Cleaning resumes...")
ds_resumes['cleaned'] = ds_resumes['Resume_str'].apply(clean_text)
print("✅ Cleaning done!")

# ── 3. Extract Skills ─────────────────────────────────────
print("\n⏳ Extracting skills...")
ds_resumes['skills'] = ds_resumes['cleaned'].apply(extract_skills)
print("✅ Skill extraction done!")

# ── 4. Job Description ────────────────────────────────────
JOB_DESCRIPTION = """
We are looking for a talented Data Science / ML Engineer to join our team.

Requirements:
- Strong programming skills in Python and R
- Experience with machine learning and deep learning
- Proficiency in SQL and database management
- Hands on experience with TensorFlow, Keras or PyTorch
- Knowledge of data analysis, data visualization and feature engineering
- Experience with cloud platforms such as AWS or Azure
- Familiarity with Docker, Git and agile development
- Strong communication and problem solving skills
- Experience with NLP and computer vision is a plus
- Knowledge of pandas, numpy, scikit-learn and matplotlib
"""

cleaned_jd = clean_text(JOB_DESCRIPTION)
jd_skills  = extract_skills(cleaned_jd)
print(f"\n✅ Job Description ready — {len(jd_skills)} skills required")

# ── 5. Score Resumes ──────────────────────────────────────
print("\n⏳ Scoring resumes...")
cleaned_resumes     = ds_resumes['cleaned'].tolist()
scores              = score_resumes(cleaned_jd, cleaned_resumes)
ds_resumes['score'] = scores
print("✅ Scoring done!")

# ── 6. Rank Candidates ────────────────────────────────────
print("\n⏳ Ranking candidates...")
ranked_df = rank_candidates(ds_resumes, jd_skills)
print("✅ Ranking done!")

# ── 7. Display Top 10 ─────────────────────────────────────
print("\n" + "=" * 50)
print("        TOP 10 CANDIDATES RANKED")
print("=" * 50)

top10 = ranked_df.head(10)
for _, row in top10.iterrows():
    print(f"\n🏅 Rank {row['Rank']} — {row['Candidate']}")
    print(f"   Score          : {row['Score']}")
    print(f"   Matched Skills : {row['Matched Skills']}/{len(jd_skills)}")
    print(f"   Skills Found   : {row['Skills Found']}")
    print(f"   Missing Skills : {row['Missing Skills']}")

# ── 8. Bar Chart ──────────────────────────────────────────
print("\n⏳ Generating charts...")

plt.figure(figsize=(12, 6))
colors = ['#2ecc71' if i == 0 else '#3498db' for i in range(len(top10))]
bars   = plt.bar(top10['Candidate'], top10['Score'], color=colors, edgecolor='white')

plt.title('Top 10 Candidates — Role Fit Score',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Candidate', fontsize=12)
plt.ylabel('Similarity Score', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.ylim(0, max(top10['Score']) + 0.05)

for bar, score in zip(bars, top10['Score']):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.005,
             str(score),
             ha='center', va='bottom',
             fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('data/candidate_scores.png', dpi=150)
plt.show()

# ── 9. Skill Heatmap ──────────────────────────────────────
skill_matrix    = []
candidate_names = []

for _, row in top10.iterrows():
    candidate_names.append(row['Candidate'])
    row_skills = [1 if skill in row['Skills Found'] else 0 for skill in jd_skills]
    skill_matrix.append(row_skills)

skill_df = pd.DataFrame(
    skill_matrix,
    index=candidate_names,
    columns=jd_skills
)

plt.figure(figsize=(18, 7))
colors_map = sns.color_palette(["#e74c3c", "#2ecc71"])

sns.heatmap(
    skill_df,
    cmap=colors_map,
    linewidths=0.5,
    linecolor='white',
    annot=True,
    fmt='d',
    cbar=False,
    annot_kws={"size": 9}
)

plt.title('Skill Coverage Map — Top 10 Candidates\n🟥 Missing Skill   🟩 Has Skill',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Required Skills', fontsize=11)
plt.ylabel('Candidates', fontsize=11)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig('data/skill_heatmap.png', dpi=150)
plt.show()

print("\n✅ Charts saved in data/ folder")
print("\n🎉 Resume Screening Complete!")
print("=" * 50)