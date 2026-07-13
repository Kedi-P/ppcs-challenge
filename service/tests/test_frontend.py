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


def test_result_status_is_an_accessible_live_region():
    # Screen readers must be told the verdict when it changes after submit.
    response = client.get("/")

    assert response.status_code == 200
    assert 'id="result-status"' in response.text
    assert 'aria-live="polite"' in response.text
    assert 'role="status"' in response.text


def test_workbench_exposes_safe_to_advertise_verdict():
    # The headline "safe to advertise" indicator lives in the result panel...
    index = client.get("/")
    assert 'id="advertise-verdict"' in index.text

    # ...and the script renders it from the API verdict with a text cue, not
    # colour alone (WCAG 1.4.1).
    script = client.get("/static/app.js")
    assert "advertiseVerdict" in script.text
    assert "Safe to advertise" in script.text
    assert "Do not advertise" in script.text


def test_frontend_script_validates_prices_before_calling_api():
    # Client-side guards for the four bad-input cases in the ticket.
    response = client.get("/static/app.js")

    assert "Number.isFinite" in response.text  # non-numeric prices
    assert "wasPrice <= 0" in response.text or "nowPrice <= 0" in response.text  # zero/negative
    assert "nowPrice > wasPrice" in response.text  # now above was
    assert "SKU is required" in response.text  # missing SKU
