from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal

def extract_lines(pdf_path):
    lines = []
    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        text = text_line.get_text().strip()
                        if not text or len(text) < 3:
                            continue  # skip short/noisy lines
                        lines.append({
                            "text": text,
                            "page": page_num,
                            "x0": text_line.x0,
                            "x1": text_line.x1,
                            "y0": text_line.y0,
                            "y1": text_line.y1,
                            "font_size": round(text_line.height, 2)
                        })
    return lines
