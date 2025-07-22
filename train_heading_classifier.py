import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import random

# ----------------------------
# 🎯 STEP 1: Labeled Headline Samples
# ----------------------------

# Simulated heading and non-heading text with labels
heading_samples = [
    # Titles (document main titles)
    ("Annual Research Report 2024", "Title"),
    ("Student Information Handbook", "Title"),
    ("Academic Calendar 2025-26", "Title"),
    ("Registration Notice - Autumn Semester", "Title"),
    ("IET Lucknow Course Catalog", "Title"),
    ("Welcome to Orientation 2025", "Title"),
    ("Mid Term Examination Schedule", "Title"),
    ("Graduation Ceremony Guidelines", "Title"),
    ("Final Year Project Rules", "Title"),

    # H1 - Major sections
    ("Important Instructions", "H1"),
    ("Course Registration", "H1"),
    ("Fee Payment Process", "H1"),
    ("Eligibility Criteria", "H1"),
    ("Hostel Allocation Policy", "H1"),
    ("Anti-Ragging Declaration", "H1"),
    ("Grading and Evaluation", "H1"),

    # H2 - Subsections
    ("Required Documents", "H2"),
    ("Late Fee Details", "H2"),
    ("Submission Timeline", "H2"),
    ("Refund Policy", "H2"),
    ("Library Facilities", "H2"),
    ("Counseling Services", "H2"),
    ("Medical Emergencies", "H2"),
    ("Contact Information", "H2"),
    ("Student Clubs", "H2"),
    ("Wi-Fi Access Procedure", "H2"),

    # H3 - Smaller nested headings
    ("In Case of Delay", "H3"),
    ("Between 10 AM to 4 PM", "H3"),
    ("Registrar’s Approval Needed", "H3"),
    ("Through Online Portal", "H3"),
    ("After Verification", "H3"),
    ("Step-by-step Instructions", "H3"),
    ("Only For Final Years", "H3"),

    # Non-headings (paragraphs or general content)
    ("The student must ensure that the details provided are accurate.", "None"),
    ("If you face any issues, please contact the administration office.", "None"),
    ("This form must be submitted to the department coordinator.", "None"),
    ("No late entries will be entertained under any circumstances.", "None"),
    ("Each student will receive a confirmation email.", "None"),
    ("The final list will be shared on the notice board.", "None"),
    ("Scanned copies are not accepted; bring originals.", "None"),
    ("Keep a soft copy of your application for records.", "None"),
    ("Candidates with medical certificates may apply for extension.", "None"),
    ("Verification will take place in Room 105.", "None")
]

# ----------------------------
# 🧠 STEP 2: Feature Generation
# ----------------------------

# Convert each labeled line into a set of numerical features
def generate_features(text, label):
    return {
        "text": text,
        "length": len(text),  # total number of characters
        "num_tokens": len(text.split()),  # number of words
        "is_title_case": int(text.istitle()),  # 1 if Title Case
        "is_all_caps": int(text.isupper()),  # 1 if fully uppercase
        "ends_with_punct": int(text[-1] in ".?!:"),  # ends with punctuation
        "starts_with_cap": int(text[0].isupper()),  # starts with capital letter
        "is_center_aligned": int(random.choice([0, 1])),  # simulated center alignment
        "y_pos": round(random.uniform(0.05, 0.95), 2),  # simulated Y position
        "capital_ratio": round(sum(1 for c in text if c.isupper()) / max(1, len(text)), 2),  # uppercase ratio
        "line_height": round(random.uniform(12.0, 18.0), 1),  # simulated line height
        "label": label
    }

# Apply feature generation to all samples
data = [generate_features(text, label) for text, label in heading_samples]
df = pd.DataFrame(data)

# ----------------------------
# 📊 STEP 3: Training Setup
# ----------------------------

# Features used for training
features = [
    "length", "num_tokens", "is_title_case", "is_all_caps",
    "ends_with_punct", "starts_with_cap", "is_center_aligned", "y_pos",
    "capital_ratio", "line_height"
]

X = df[features]       # feature matrix
y = df["label"]        # target labels

# Split data into training and testing (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# 🏗️ STEP 4: Train Classifier
# ----------------------------

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ----------------------------
# 🧪 STEP 5: Evaluate Model
# ----------------------------

print("\n📊 Classification Report (50+ Realistic Samples):")
print(classification_report(y_test, clf.predict(X_test)))

# ----------------------------
# 💾 STEP 6: Save Trained Model
# ----------------------------

joblib.dump(clf, "model/heading_classifier.pkl")
print("✅ Model saved to: model/heading_classifier.pkl")
