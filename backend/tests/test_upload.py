import io
import zipfile

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def make_zip(files: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buffer.getvalue()


def upload(data: bytes, filename: str = "project.zip"):
    return client.post(
        "/api/projects",
        files={"file": (filename, data, "application/zip")},
    )


def test_valid_zip_is_accepted():
    response = upload(make_zip({"app/main.py": "print('hi')"}))
    assert response.status_code == 200


def test_zip_slip_is_rejected():
    response = upload(make_zip({"../../x.py": "print('hacked')"}))
    assert response.status_code == 400


def test_non_zip_extension_is_rejected():
    response = upload(b"hello", filename="notes.txt")
    assert response.status_code == 400


def test_fake_zip_is_rejected():
    response = upload(b"this is not a zip", filename="fake.zip")
    assert response.status_code == 400