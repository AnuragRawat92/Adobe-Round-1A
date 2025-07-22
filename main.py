import os
import json
import re
from utils.extractor import extract_lines
from utils.classifier import classify_lines

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def is_valid_title(text):
    return (
        len(text.strip()) >= 10 and
        not text.strip().startswith("(") and
        not re.match(r"^\(?Prof\.|\(?Dr\.", text.strip(), re.IGNORECASE) and
        not text.strip().lower().startswith("copy to")
    )

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(INPUT_DIR, filename)
            lines = extract_lines(path)
            heading_data = classify_lines(lines)

            # Get valid title or fallback
            title = next(
                (h["text"] for h in heading_data if h["level"] == "Title" and is_valid_title(h["text"])),
                os.path.splitext(filename)[0].replace("_", " ")
            )

            outline = [h for h in heading_data if h["level"] != "Title"]

            # Ensure output directory exists
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            # Save output
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({
                    "title": title,
                    "outline": outline
                }, f, indent=2, ensure_ascii=False)

            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    main()
