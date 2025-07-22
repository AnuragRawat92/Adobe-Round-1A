def generate_features(line):
    """
    Generate a set of numerical and boolean features from a line of text
    for use in a machine learning heading classifier.

    Parameters:
        line (dict): A dictionary representing a text line with layout info

    Returns:
        features (dict): Extracted features used for classification
    """
    text = line["text"]

    features = {
        # 📏 Total character length of the line
        "length": len(text),

        # 🔢 Number of words (tokens) in the line
        "num_tokens": len(text.split()),

        # 📝 Checks if the text is in Title Case (e.g., "Introduction To AI")
        "is_title_case": text.istitle(),

        # 🔠 Checks if the entire line is in uppercase (shouts/headings)
        "is_all_caps": text.isupper(),

        # ❗ Checks if line ends with punctuation like .?!:
        "ends_with_punct": text[-1] in ".?!:" if text else 0,

        # 🔡 Checks if the first character is uppercase
        "starts_with_cap": text[0].isupper() if text else 0,

        # 🎯 Check if text is center-aligned (assumes center ≈ 300px, tolerance ±100)
        "is_center_aligned": abs((line["x0"] + line["x1"]) / 2 - 300) < 100,

        # 🧭 Vertical position normalized to [0, 1] (top = 1, bottom = 0 approx)
        "y_pos": round(line["y1"] / 800, 2),

        # 🔠 Ratio of capital letters to total characters (e.g., for acronyms or titles)
        "capital_ratio": sum(1 for c in text if c.isupper()) / max(1, len(text)),

        # 📐 Approximate line height (helps separate headings from paragraphs)
        "line_height": round(line["y1"] - line["y0"], 2)
    }

    return features
