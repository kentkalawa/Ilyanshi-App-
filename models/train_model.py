import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load data
df = pd.read_csv("../data/complaints.csv")
print(f"Loaded {len(df)} complaints")

# Prepare features
X = df["complaint_text"]
y_subject = df["subject"]
y_urgency = df["urgency"]
y_sentiment = df["sentiment"]

# Vectorize text
vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
X_vec = vectorizer.fit_transform(X)

# Train models
print("Training models...")

# Subject classifier
X_train, X_test, y_train, y_test = train_test_split(X_vec, y_subject, test_size=0.2, random_state=42)
subject_model = LogisticRegression(max_iter=1000)
subject_model.fit(X_train, y_train)
subject_acc = accuracy_score(y_test, subject_model.predict(X_test))
print(f"Subject classifier accuracy: {subject_acc:.2f}")

# Urgency classifier
X_train, X_test, y_train, y_test = train_test_split(X_vec, y_urgency, test_size=0.2, random_state=42)
urgency_model = LogisticRegression(max_iter=1000)
urgency_model.fit(X_train, y_train)
urgency_acc = accuracy_score(y_test, urgency_model.predict(X_test))
print(f"Urgency classifier accuracy: {urgency_acc:.2f}")

# Sentiment classifier
X_train, X_test, y_train, y_test = train_test_split(X_vec, y_sentiment, test_size=0.2, random_state=42)
sentiment_model = LogisticRegression(max_iter=1000)
sentiment_model.fit(X_train, y_train)
sentiment_acc = accuracy_score(y_test, sentiment_model.predict(X_test))
print(f"Sentiment classifier accuracy: {sentiment_acc:.2f}")

# Save models
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(subject_model, "subject_model.pkl")
joblib.dump(urgency_model, "urgency_model.pkl")
joblib.dump(sentiment_model, "sentiment_model.pkl")

print("✅ Models saved to models/ folder")