from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_resumes(cleaned_jd, cleaned_resumes):
    """
    Scores each resume against the job description
    using TF-IDF vectorization and cosine similarity.
    
    Returns a list of scores between 0 and 1.
    Higher score = better match.
    """
    # Step 1 — Combine JD + all resumes into one list
    corpus = [cleaned_jd] + cleaned_resumes

    # Step 2 — Convert text to numbers (TF-IDF vectors)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Step 3 — Get JD vector (first item)
    jd_vector = tfidf_matrix[0]

    # Step 4 — Get all resume vectors (rest of items)
    resume_vectors = tfidf_matrix[1:]

    # Step 5 — Calculate cosine similarity scores
    scores = cosine_similarity(jd_vector, resume_vectors)[0]

    # Step 6 — Round scores to 4 decimal places
    scores = [round(float(s), 4) for s in scores]

    return scores