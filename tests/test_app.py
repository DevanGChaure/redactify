import io
import pytest
from PIL import Image
from app import app
from database.db import init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as c:
        yield c


def make_test_image():
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_upload_valid_file(client):
    data = {
        "document": (make_test_image(), "sample.png")
    }
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code in (200, 302)


def test_upload_invalid_file_rejected(client):
    data = {
        "document": (io.BytesIO(b"not a real file"), "malware.exe")
    }
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
