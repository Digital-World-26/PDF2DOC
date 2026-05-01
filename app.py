from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["pdf"]

    if file.filename == "":
        return "No file selected"

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    docx_filename = file.filename.replace(".pdf", ".docx")
    docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

    # 🔥 Convert PDF → Word
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

    return send_file(docx_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
