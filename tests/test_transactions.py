def test_money_transfer(client):
    from tests.test_accounts import get_auth_token
    token = get_auth_token(client, "transfer@test.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Account A
    resp_a = client.post("/accounts", json={"initial_deposit": 1000}, headers=headers)
    assert resp_a.status_code == 201
    acc_a = resp_a.json()
    
    # Create Account B
    resp_b = client.post("/accounts", json={"initial_deposit": 0}, headers=headers)
    assert resp_b.status_code == 201
    acc_b = resp_b.json()
    
    # Transfer 500 from A to B
    resp_transfer = client.post(
        "/transactions/transfer",
        json={"to_account": acc_b["account_number"], "amount": 500},
        headers=headers
    )
    assert resp_transfer.status_code == 200
    transfer_data = resp_transfer.json()
    assert transfer_data["status"] == "success"
    
    # Check balances
    resp_a_check = client.get(f"/accounts/{acc_a['id']}", headers=headers)
    assert resp_a_check.json()["balance"] == 500
    
    resp_b_check = client.get(f"/accounts/{acc_b['id']}", headers=headers)
    assert resp_b_check.json()["balance"] == 500
