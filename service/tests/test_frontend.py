from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_workbench_index_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "PPCS Workbench" in response.text
    assert "/static/app.js" in response.text
    assert "/static/styles.css" in response.text


def test_frontend_script_calls_validate_without_browser_persistence():
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert 'fetch("/validate"' in response.text
    assert "localStorage" not in response.text
    assert "console.log" not in response.text
