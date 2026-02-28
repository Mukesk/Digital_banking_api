def get_auth_token(client, email="acc@test.com"):
    # register
    client.post("/auth/register", json={"email": email, "password": "pass", "role": "customer"})
    # login
    resp = client.post("/auth/login", data={"username": email, "password": "pass"})
    return resp.json()["access_token"]

def test_create_account(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/accounts",
        json={"initial_deposit": 5000},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["balance"] == 5000
    assert "account_number" in data
    assert data["status"] == "active"
