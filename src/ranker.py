import pandas as pd

def rank_candidates(df, jd_skills):
    """
    Ranks candidates by score and identifies
    matched and missing skills for each candidate.
    """
    results = []

    for i, row in df.iterrows():
        candidate_skills = set(row['skills'])
        required_skills  = set(jd_skills)

        # Skills the candidate HAS that match JD
        matched_skills = candidate_skills & required_skills

        # Skills the candidate is MISSING from JD
        missing_skills = required_skills - candidate_skills

        results.append({
            "Candidate"      : f"Candidate {i+1}",
            "Score"          : row['score'],
            "Matched Skills" : len(matched_skills),
            "Skills Found"   : list(matched_skills),
            "Missing Skills" : list(missing_skills)
        })

    # ── Sort by score highest to lowest ──────────────────
    ranked_df = pd.DataFrame(results)
    ranked_df = ranked_df.sort_values("Score", ascending=False)
    ranked_df = ranked_df.reset_index(drop=True)
    ranked_df["Rank"] = ranked_df.index + 1

    return ranked_df