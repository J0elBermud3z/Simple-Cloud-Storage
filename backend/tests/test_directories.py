import os
import uuid


def test_01_create_directory(client):
    
    test_directory_name = f"test_directory_{uuid.uuid4().hex[:6]}"


    response = client.post(
        f"/api/folder/{test_directory_name}"
    )

    response_content = response.json
    assert response.status_code == 201
    assert response_content['status'] == 'success'
    assert response_content['data']['name'] == test_directory_name
    assert response_content['data']['type'] == 'directory'
    
    
def test_02_get_created_directory(client):
    
    test_directory_name = f"test_directory_{uuid.uuid4().hex[:6]}"
    client.post(f"/api/folder/{test_directory_name}")

    response = client.get("/api/folder/")
    directories = [directory['name'] for directory in response.json['data']['directories']]
    assert response.status_code == 200
    assert test_directory_name in directories

def test_03_rename_directory(client):
    
    test_directory_name = f"test_directory_{uuid.uuid4().hex[:6]}"
    client.post(f"/api/folder/{test_directory_name}")
    
    new_name = f"renamed_{test_directory_name}"
    response = client.patch(f"/api/folder/{test_directory_name}", json={'name': new_name})
    assert response.status_code == 200
    assert response.json['status'] == 'success'


    response = client.patch(f"/api/folder/{new_name}", json={'name': test_directory_name})
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_04_delete_directory(client):

    test_directory_name = f"test_directory_{uuid.uuid4().hex[:6]}"
    client.post(f"/api/folder/{test_directory_name}")

    response = client.delete(f"/api/folder/{test_directory_name}")
    assert response.status_code == 200
    assert response.json['status'] == 'success'