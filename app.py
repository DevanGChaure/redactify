import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify

from database.db import init_db, insert_document, get_all_documents, get_document

from redaction.detector import extract_text
from database.db import (
    init_db, insert_document, get_all_documents,
    get_document, update_extracted_text
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    documents = get_all_documents()[:5]  # recent 5
    return render_template("index.html", documents=documents)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    file = request.files.get("document")
    if not file or file.filename == "":
        return render_template("upload.html", error="No file selected"), 400

    if not allowed_file(file.filename):
        return render_template("upload.html", error="Unsupported file type"), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    stored_filename = f"{uuid.uuid4().hex}.{ext}"
    saved_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_filename)
    file.save(saved_path)

    doc_id = insert_document(file.filename, stored_filename)

    try:
        text = extract_text(saved_path)
        update_extracted_text(doc_id, text, status="extracted")
    except Exception as e:
        update_extracted_text(doc_id, "", status="extraction_failed")

    return redirect(url_for("history"))


@app.route("/history")
def history():
    documents = get_all_documents()
    return render_template("history.html", documents=documents)


@app.route("/api/documents")
def api_documents():
    return jsonify({"documents": get_all_documents()})


@app.route("/health")
def health():
    commit = os.environ.get("RENDER_GIT_COMMIT", "local-dev")
    return jsonify({"status": "ok", "commit": commit})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)