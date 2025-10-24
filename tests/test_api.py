import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Ensure /healthz endpoint works"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_analyze_docx():
    """Upload a DOCX file and get a compliance report"""
    sample_path = os.path.join("sample_docs", "sample.docx")
    with open(sample_path, "rb") as f:
        response = client.post(
            "/v1/analyze",
            files={"file": ("sample.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert "document_id" in data
    assert isinstance(data["report"]["issues"], list)


def test_rewrite_flow():
    """Full flow: analyze -> rewrite -> download"""
    sample_path = os.path.join("sample_docs", "sample.docx")
    # Step 1: analyze
    with open(sample_path, "rb") as f:
        analyze_res = client.post(
            "/v1/analyze",
            files={"file": ("sample.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
    assert analyze_res.status_code == 200
    doc_id = analyze_res.json()["document_id"]

    # Step 2: rewrite
    rewrite_res = client.post(
        "/v1/rewrite",
        json={"document_id": doc_id, "strategy": "auto"},
    )
    assert rewrite_res.status_code == 200
    out_name = rewrite_res.json()["download_filename"]

    # Step 3: download
    download_res = client.get(f"/v1/download/{out_name}")
    assert download_res.status_code == 200
    assert download_res.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
