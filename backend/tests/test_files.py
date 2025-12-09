import os
import uuid
import io

def test_01_create_file(client):
    
    test_file_name = f"test_file_{uuid.uuid4().hex[:6]}.txt"
    file_content = b"contenido de prueba"

    data = {
        'file': (io.BytesIO(file_content), test_file_name)
    }

    response = client.post(
        "/api/file/",
        data=data,
        content_type='multipart/form-data'
    )

    response_content = response.json
    assert response.status_code == 201
    assert response_content['status'] == 'success'
    assert response_content['data']['name'] == test_file_name
    assert response_content['data']['type'] == 'file'

def test_02_get_created_file(client):

    test_file_name = f"test_file_{uuid.uuid4().hex[:6]}.txt"
    file_content = b"contenido de prueba"
    client.post(
        "/api/file/",
        data={'file': (io.BytesIO(file_content), test_file_name)},
        content_type='multipart/form-data'
    )

    response = client.get("/api/folder/") 
    files = [file['name'] for file in response.json['data']['files']]
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert test_file_name in files


def test_03_rename_file(client):
    
    test_file_name = f"test_file_{uuid.uuid4().hex[:6]}.txt"
    file_content = b"contenido de prueba"
    client.post(
        "/api/file/",
        data={'file': (io.BytesIO(file_content), test_file_name)},
        content_type='multipart/form-data'
    )
    
    new_name = f"renamed_{test_file_name}"
    response = client.patch(f"/api/file/{test_file_name}", json={'name': new_name})
    assert response.status_code == 200
    assert response.json['status'] == 'success'



def test_04_size_file(client):
    
    test_file_name = f"test_file_{uuid.uuid4().hex[:6]}.txt"
    file_content = b"contenido de prueba"
    client.post(
        "/api/file/",
        data={'file': (io.BytesIO(file_content), test_file_name)},
        content_type='multipart/form-data'
    )
    
    response = client.get(f"/api/file/{test_file_name}")
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_05_delete_file(client):

    test_file_name = f"test_file_{uuid.uuid4().hex[:6]}.txt"
    file_content = b"contenido de prueba"
    client.post(
        "/api/file/",
        data={'file': (io.BytesIO(file_content), test_file_name)},
        content_type='multipart/form-data'
    )

    response = client.delete(f"/api/file/{test_file_name}")
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    response = client.get(f"/api/file/{test_file_name}")
    assert response.status_code == 404
