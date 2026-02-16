def test_create_list_delete_task(client, token):
    # Create
    res = client.post(
        "/api/tasks",
        json={"title": "Test task", "status": "backlog", "priority": "medium"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 201
    created = res.get_json()
    task_id = created["id"]
    assert created["title"] == "Test task"
    # List
    res_list = client.get(
        "/api/tasks?limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_list.status_code == 200
    items = res_list.get_json()["items"]
    assert any(t["id"] == task_id for t in items)
    # Delete
    res_del = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_del.status_code == 200

