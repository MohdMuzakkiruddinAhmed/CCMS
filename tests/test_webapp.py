"""Unit tests for the CCMS Flask web application."""
import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "webapp"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webapp.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["UPLOAD_FOLDER"] = "/tmp/ccms_test_uploads"
    os.makedirs(flask_app.config["UPLOAD_FOLDER"], exist_ok=True)
    with flask_app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_post_no_files(client):
    response = client.post("/")
    assert response.status_code in (200, 302)


def test_index_post_with_files(client):
    er1_content = b"RecID,ClusterID\n1,a\n2,b\n3,b\n"
    er2_content = b"RecID,ClusterID\n1,x\n2,y\n3,y\n"

    data = {
        "file1": (er1_content, "er1.csv", "text/csv"),
        "file2": (er2_content, "er2.csv", "text/csv"),
    }

    from io import BytesIO
    response = client.post(
        "/",
        data={
            "file1": (BytesIO(er1_content), "er1.csv"),
            "file2": (BytesIO(er2_content), "er2.csv"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert b"Unchanged" in response.data or b"Results" in response.data
