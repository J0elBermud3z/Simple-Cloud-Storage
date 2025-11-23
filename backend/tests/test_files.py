import requests
import os
import uuid


BASE_URL = "http://localhost:80/api"
TEST_FILE_NAME = f"test_file_{uuid.uuid4().hex[:6]}.txt"
TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), TEST_FILE_NAME)

def test_01_create_file():
    
    with open(TEST_FILE_PATH, "wb") as f:
        f.write(b"contenido de prueba")

    with open(TEST_FILE_PATH, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/file/",
            files={"file": (TEST_FILE_NAME, f, "text/plain")}
        )

    response_content = response.json()
    assert response.status_code == 200
    assert response_content['status'] == 'success'
    assert response_content['data']['name'] == TEST_FILE_NAME
    assert response_content['data']['type'] == 'file'

def test_02_get_created_file():

    response = requests.get(f"{BASE_URL}/")
    files    = [file['name'] for file in response.json()['data']['files']]
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert TEST_FILE_NAME in files


def test_03_rename_file():
    
    new_name = f"renamed_{TEST_FILE_NAME}"
    response = requests.patch(f"{BASE_URL}/{TEST_FILE_NAME}/{new_name}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'

    response = requests.patch(f"{BASE_URL}/{new_name}/{TEST_FILE_NAME}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_04_size_file():
    
    response = requests.get(f"{BASE_URL}/size?path={TEST_FILE_NAME}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_05_delete_file():

    response = requests.delete(f"{BASE_URL}/{TEST_FILE_NAME}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'

    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
