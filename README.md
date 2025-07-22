📄 **Adobe Hackathon 2025 — PDF Outline Extractor (Round 1A)**

This is a machine learning-based solution for extracting document outlines (Title, H1, H2, H3) from PDFs for the Adobe India Hackathon 2025.

**Features:**  
✅ No font-size hardcoding  
✅ ML-based heading detection  
✅ CLI + Flask API supported  
✅ Docker-ready  
✅ Handles real-world layout variations

**Folder Structure:**  
project/  
├── app.py (Flask API server)  
├── main.py (CLI batch extractor)  
├── train_heading_classifier.py (ML training script)  
├── requirements.txt (Dependencies)  
├── Dockerfile (Docker image setup)  
├── input/ (Input PDF files)  
├── output/ (Output JSON files)  
├── model/  
│   └── heading_classifier.pkl (Trained classifier model)  
├── utils/  
│   ├── extractor.py (PDF text extraction logic)  
│   ├── classifier.py (Heading prediction logic)  
│   └── features.py (Feature generation for ML)

---

**🔧 Setup Instructions (Local):**

**Step 1: Create and activate virtual environment**  
`python -m venv venv`  
On Windows: `venv\Scripts\activate`  
On Linux/macOS: `source venv/bin/activate`

**Step 2: Install required dependencies**  
`pip install -r requirements.txt`

---

**🧠 Train the Model (ML-based Heading Detection):**  
`python train_heading_classifier.py`  
Output: `model/heading_classifier.pkl`

---

**🏃 Run Locally on PDFs:**  
Place PDFs in the `input/` folder (e.g., `input/sample.pdf`)  
Run the extractor:  
`python main.py`  
Output saved in `output/` as JSON.

**Example Output:**  
{
  "title": "Student Handbook",
  "outline": [
    { "level": "H1", "text": "Instructions", "page": 1 },
    { "level": "H2", "text": "Late Fee", "page": 1 }
  ]
}

---

**🌐 Run with Flask API:**  
Start server: `python app.py`  
Send a request:  
`curl -X POST http://localhost:5000/extract -F "pdf=@input/sample.pdf"`

**Example Response:**  
{
  "title": "Academic Calendar",
  "outline": [
    { "level": "H1", "text": "Dates", "page": 1 }
  ]
}

---

**🐳 Docker Setup 

**Step 1: Dockerfile**  
```
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p input output
CMD ["python", "main.py"]
```

**Step 2: Build Docker image**  
`docker build -t adobe-heading-extractor .`

**Step 3: Run extraction in Docker**  
`docker run -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output adobe-heading-extractor`

**Run Flask API inside Docker:**  
`docker run -p 5000:5000 adobe-heading-extractor`

---

**📦 requirements.txt:**  
pdfminer.six==20221105
joblib==1.3.2
numpy>=1.26.0
scikit-learn==1.3.2
joblib==1.3.2
pandas==2.2.2
---

**🔒 Constraints Met:**  
❌ No font-size heuristics  
✅ ML-based detection  
❌ No API/web calls  
✅ Compact model & fast runtime  
✅ Works on multiple types of PDFs

---

**📞 Contact:**  
Developed by: **CP_Haters**  
📍 IET Lucknow  
💻 For: Adobe India Hackathon 2025

---

**🧪 Sample Output Format:**  
{
  "title": "Registration Notice 2025",
  "outline": [
    { "level": "H1", "text": "Date of Registration", "page": 1 },
    { "level": "H2", "text": "Required Documents", "page": 1 }
  ]
}
