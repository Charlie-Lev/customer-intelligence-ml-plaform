from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


VALID_CUSTOMER = {
    "customer_id": "NT-000001",
    "age": 32.0,
    "tenure_months": 27,
    "monthly_fee": 101.65,
    "total_spent": 2467.19,
    "support_calls": 0,
    "complaints": 0,
    "last_payment_delay": 3,
    "digital_usage_score": 80.4,
    "marketing_score": 91.0,
    "preferred_contact_hour": 15,
    "gender": "Femenino",
    "region": "Sur",
    "customer_segment": "Masivo",
    "contract_type": "Bianual",
    "internet_service": "Fibra",
    "tv_service": "No",
    "streaming_service": "Sí",
    "payment_method": "Efectivo",
}


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_valid():
    response = client.post("/predict", json=VALID_CUSTOMER)
    assert response.status_code == 200
    body = response.json()
    assert "churn_probability" in body
    assert "churn_prediction" in body


def test_predict_invalid_age():
    payload = {**VALID_CUSTOMER, "age": -5}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_batch_valid():
    csv_text = (
        ",".join(VALID_CUSTOMER.keys())
        + "\n"
        + ",".join(str(value) for value in VALID_CUSTOMER.values())
        + "\n"
    )
    response = client.post(
        "/predict/batch",
        files={"file": ("sample.csv", csv_text, "text/csv")},
    )
    assert response.status_code == 200
    assert "churn_probability" in response.text


def test_batch_non_csv():
    response = client.post(
        "/predict/batch",
        files={"file": ("sample.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


def test_batch_empty():
    response = client.post(
        "/predict/batch",
        files={"file": ("empty.csv", b"", "text/csv")},
    )
    assert response.status_code == 400


def test_openapi_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/predict" in response.json()["paths"]