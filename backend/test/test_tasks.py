def test_create_task(client, token):
    res = client.post(
        "/tasks",
        json={"title": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 201

