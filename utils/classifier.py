import joblib
from .features import generate_features

MODEL_PATH = "model/heading_classifier.pkl"
clf = joblib.load(MODEL_PATH)

def classify_lines(lines):
    headings = []
    for line in lines:
        feats = generate_features(line)
        X = [[
            feats["length"],
            feats["num_tokens"],
            feats["is_title_case"],
            feats["is_all_caps"],
            feats["ends_with_punct"],
            feats["starts_with_cap"],
            feats["is_center_aligned"],
            feats["y_pos"],
            feats["capital_ratio"],
            feats["line_height"]
        ]]
        pred = clf.predict(X)[0]
        if pred in ["Title", "H1", "H2", "H3"]:
            headings.append({
                "level": pred,
                "text": line["text"],
                "page": line["page"]
            })
    return headings
