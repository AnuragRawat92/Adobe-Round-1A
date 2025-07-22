from flask import Flask, request, jsonify
import os
import tempfile
import joblib
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal

# ----------------------------------------
# 📌 ML Feature Generator
def generate_features(line):
    text = line["text"]
    return {
        "length": len(text),
        "num_tokens": len(text.split()),
        "is_title_case": text.istitle(),
        "is_all_caps": text.isupper(),
        "ends_with_punct": text[-1] in ".?!:",
        "starts_with_cap": text[0].isupper(),
        "is_center_aligned": abs((line["x0"] + line["x1"]) / 2 - 300) < 100,
        "y_pos": round(line["y1"] / 800, 2),
        "capital_ratio": round(sum(1 for c in text if c.isupper()) / max(1, len(text)), 2),
        "line_height": 15.0
    }

# ----------------------------------------
# 📌 Load Trained Model
MODEL_PATH = "model/heading_classifier.pkl"
clf = joblib.load(MODEL_PATH)

# ----------------------------------------
# 📌 Line Extractor from PDF
def extract_lines(pdf_path):
    lines = []
    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        text = text_line.get_text().strip()
                        if text:
                            lines.append({
                                "text": text,
                                "page": page_num,
                                "x0": text_line.x0,
                                "x1": text_line.x1,
                                "y0": text_line.y0,
                                "y1": text_line.y1
                            })
    return lines

# ----------------------------------------
# 📌 Classify Extracted Lines
def classify_lines(lines):
    headings = []
    for line in lines:
        feats = generate_features(line)
        X = [[
            feats["length"], feats["num_tokens"],
            feats["is_title_case"], feats["is_all_caps"],
            feats["ends_with_punct"], feats["starts_with_cap"],
            feats["is_center_aligned"], feats["y_pos"],
            feats["capital_ratio"], feats["line_height"]
        ]]
        pred = clf.predict(X)[0]
        if pred in ["Title", "H1", "H2", "H3"]:
            headings.append({
                "level": pred,
                "text": line["text"],
                "page": line["page"]
            })
    return headings

# ----------------------------------------
# 🚀 Flask App Starts Here
app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_headings():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    # Save uploaded PDF to a temporary file
    file = request.files["pdf"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        file.save(temp.name)
        lines = extract_lines(temp.name)
        headings = classify_lines(lines)

    # Extract title and outline from headings
    title = next((h["text"] for h in headings if h["level"] == "Title"), "Untitled Document")
    outline = [h for h in headings if h["level"] != "Title"]
    
    return jsonify({"title": title, "outline": outline})

# ----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
