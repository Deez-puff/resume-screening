import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ── Download required NLTK data ───────────────────────────
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# ── Initialize ────────────────────────────────────────────
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Cleans raw resume text:
    - Lowercases everything
    - Removes special characters & numbers
    - Removes stopwords (the, is, and...)
    - Lemmatizes words (running → run)
    """
    # Step 1 — Lowercase
    text = text.lower()

    # Step 2 — Remove special characters, numbers, punctuation
    text = re.sub(r'[^a-z\s]', ' ', text)

    # Step 3 — Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 4 — Remove stopwords & lemmatize
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]

    return ' '.join(tokens)