# ============================================================
# Resume Screening & Ranking System — Web App
# Built with Streamlit
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('src')

from preprocessor import clean_text
from skill_extractor import extract_skills, SKILLS
from scorer import score_resumes
from ranker import rank_candidates

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────
st.title("📄 Resume Screening & Ranking System")
st.markdown("Upload a resume dataset, enter a job description and let ML rank your candidates automatically.")
st.divider()

# ── Step 1: Upload Dataset ────────────────────────────────
st.header("Step 1 — Upload Resume Dataset")
uploaded_file = st.file_uploader(
    "Upload your CSV file (must have a text column with resume content)",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success(f"✅ Dataset loaded — {len(df)} resumes found!")

    # ── Show preview ─────────────────────────────────────
    with st.expander("👀 Preview Dataset"):
        st.dataframe(df.head())

    st.divider()

    # ── Step 2: Select Columns ────────────────────────────
    st.header("Step 2 — Configure Your Dataset")

    col1, col2 = st.columns(2)

    with col1:
        text_column = st.selectbox(
            "Which column contains the resume text?",
            options=df.columns.tolist()
        )

    with col2:
        category_column = st.selectbox(
            "Which column contains the job category? (optional)",
            options=["None"] + df.columns.tolist()
        )

    # ── Step 3: Filter by Category ────────────────────────
    if category_column != "None":
        categories = df[category_column].unique().tolist()
        selected_category = st.selectbox(
            "Filter by job category:",
            options=["All"] + categories
        )

        if selected_category != "All":
            df = df[df[category_column] == selected_category].reset_index(drop=True)
            st.info(f"📂 Filtered to {len(df)} resumes in '{selected_category}'")

    st.divider()

    # ── Step 4: Job Description ───────────────────────────
    st.header("Step 3 — Enter Job Description")

    job_description = st.text_area(
        "Paste or type the job description here:",
        height=200,
        placeholder="""We are looking for a Data Science / ML Engineer.

Requirements:
- Strong programming skills in Python and R
- Experience with machine learning and deep learning
- Proficiency in SQL and database management
- Knowledge of TensorFlow, Keras or PyTorch
- Experience with AWS or Azure
- Familiarity with Docker and Git
- Strong communication and problem solving skills"""
    )

    # ── Step 5: Screen Button ─────────────────────────────
    st.divider()
    screen_button = st.button("🚀 Screen & Rank Resumes", type="primary", use_container_width=True)

    if screen_button:
        if not job_description.strip():
            st.error("❌ Please enter a job description first!")
        else:
            # ── Progress Bar ──────────────────────────────
            progress = st.progress(0, text="Starting...")

            # ── Clean Resumes ─────────────────────────────
            progress.progress(20, text="⏳ Cleaning resumes...")
            df['cleaned'] = df[text_column].astype(str).apply(clean_text)

            # ── Extract Skills ────────────────────────────
            progress.progress(40, text="⏳ Extracting skills...")
            df['skills'] = df['cleaned'].apply(extract_skills)

            # ── Clean JD ─────────────────────────────────
            progress.progress(60, text="⏳ Processing job description...")
            cleaned_jd = clean_text(job_description)
            jd_skills  = extract_skills(cleaned_jd)

            # ── Score ─────────────────────────────────────
            progress.progress(80, text="⏳ Scoring resumes...")
            cleaned_resumes = df['cleaned'].tolist()
            scores          = score_resumes(cleaned_jd, cleaned_resumes)
            df['score']     = scores

            # ── Rank ──────────────────────────────────────
            progress.progress(90, text="⏳ Ranking candidates...")
            ranked_df = rank_candidates(df, jd_skills)

            progress.progress(100, text="✅ Done!")

            st.divider()

            # ── Results Header ────────────────────────────
            st.header("📊 Screening Results")

            top_n = st.slider("Show top N candidates:", 5, 20, 10)
            top_df = ranked_df.head(top_n)

            # ── Metrics Row ───────────────────────────────
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Resumes Screened", len(df))
            m2.metric("Skills Required", len(jd_skills))
            m3.metric("Top Score", top_df['Score'].max())
            m4.metric("Avg Score", round(top_df['Score'].mean(), 4))

            st.divider()

            # ── Ranked Table ──────────────────────────────
            st.subheader("🏅 Ranked Candidates Table")
            display_df = top_df[['Rank', 'Candidate', 'Score', 'Matched Skills']].copy()
            display_df['Score'] = display_df['Score'].apply(lambda x: f"{x:.4f}")
            display_df['Match %'] = top_df['Matched Skills'].apply(
                lambda x: f"{round(x/len(jd_skills)*100)}%" if len(jd_skills) > 0 else "0%"
            )
            st.dataframe(display_df, use_container_width=True)

            st.divider()

            # ── Bar Chart ─────────────────────────────────
            st.subheader("📊 Candidate Score Chart")
            fig1, ax1 = plt.subplots(figsize=(12, 5))
            colors = ['#2ecc71' if i == 0 else '#3498db' for i in range(len(top_df))]
            bars   = ax1.bar(top_df['Candidate'], top_df['Score'], color=colors, edgecolor='white')

            ax1.set_title('Candidate Ranking by Role Fit Score', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Candidate')
            ax1.set_ylabel('Similarity Score')
            ax1.set_ylim(0, max(top_df['Score']) + 0.05)
            plt.xticks(rotation=45, ha='right')

            for bar, score in zip(bars, top_df['Score']):
                ax1.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.002,
                         str(score),
                         ha='center', va='bottom',
                         fontsize=8, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig1)

            st.divider()

            # ── Skill Heatmap ─────────────────────────────
            st.subheader("🟩🟥 Skill Coverage Heatmap")

            if len(jd_skills) > 0:
                skill_matrix    = []
                candidate_names = []

                for _, row in top_df.iterrows():
                    candidate_names.append(row['Candidate'])
                    row_skills = [1 if skill in row['Skills Found'] else 0 for skill in jd_skills]
                    skill_matrix.append(row_skills)

                skill_df = pd.DataFrame(
                    skill_matrix,
                    index=candidate_names,
                    columns=jd_skills
                )

                fig2, ax2 = plt.subplots(figsize=(18, 6))
                colors_map = sns.color_palette(["#e74c3c", "#2ecc71"])

                sns.heatmap(
                    skill_df,
                    cmap=colors_map,
                    linewidths=0.5,
                    linecolor='white',
                    annot=True,
                    fmt='d',
                    cbar=False,
                    annot_kws={"size": 9},
                    ax=ax2
                )

                ax2.set_title('Skill Coverage Map\n🟥 Missing Skill   🟩 Has Skill',
                              fontsize=13, fontweight='bold')
                ax2.set_xlabel('Required Skills')
                ax2.set_ylabel('Candidates')
                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.tight_layout()
                st.pyplot(fig2)
            else:
                st.warning("⚠️ No matching skills found in the job description. Try adding more specific skills.")

            st.divider()

            # ── Skill Gap Details ─────────────────────────
            st.subheader("🔍 Skill Gap Details")
            for _, row in top_df.iterrows():
                with st.expander(f"🏅 Rank {row['Rank']} — {row['Candidate']} (Score: {row['Score']})"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**✅ Skills Found:**")
                        if row['Skills Found']:
                            for skill in row['Skills Found']:
                                st.markdown(f"- 🟩 {skill}")
                        else:
                            st.markdown("None found")
                    with c2:
                        st.markdown("**❌ Missing Skills:**")
                        if row['Missing Skills']:
                            for skill in row['Missing Skills']:
                                st.markdown(f"- 🟥 {skill}")
                        else:
                            st.markdown("No missing skills!")

else:
    # ── Empty State ───────────────────────────────────────
    st.info("👆 Please upload a CSV file to get started.")
    st.markdown("""
    ### 📋 How to use this app:
    1. **Upload** any CSV file containing resume text
    2. **Select** which column has the resume content
    3. **Filter** by job category (optional)
    4. **Enter** a job description
    5. **Click** Screen & Rank Resumes
    6. **View** ranked candidates, charts and skill gaps
    
    ### 📥 Need a dataset?
    Download one here → [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
    """)