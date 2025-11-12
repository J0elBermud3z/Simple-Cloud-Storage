import requests
import os
import uuid
import shutil

BASE_URL = "http://localhost:80/api"
TEST_DIRECTORY_NAME = f"test_directory_{uuid.uuid4().hex[:6]}"
TEST_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), TEST_DIRECTORY_NAME)


def test_01_create_directory():

    if not os.path.exists(TEST_DIRECTORY_PATH):
        os.mkdir(TEST_DIRECTORY_PATH)

    response = requests.post(
        f"{BASE_URL}/folder/{TEST_DIRECTORY_NAME}"
    )

    response_content = response.json()
    assert response.status_code == 200
    assert response_content['status'] == 'success'
    assert response_content['data']['name'] == TEST_DIRECTORY_NAME
    assert response_content['data']['type'] == 'directory'
    

def test_02_get_created_directory():

    response = requests.get(f"{BASE_URL}/")
    directories    = [directory['name'] for directory in response.json()['data']['directories']]
    assert response.status_code == 200
    assert TEST_DIRECTORY_NAME in directories


def test_03_rename_directory():
    
    new_name = f"renamed_{TEST_DIRECTORY_NAME}"
    response = requests.patch(f"{BASE_URL}/{TEST_DIRECTORY_NAME}/{new_name}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'

    response = requests.patch(f"{BASE_URL}/{new_name}/{TEST_DIRECTORY_NAME}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_04_delete_directory():

    response = requests.delete(f"{BASE_URL}/{TEST_DIRECTORY_NAME}")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'

    if os.path.exists(TEST_DIRECTORY_PATH):
        shutil.rmtree(TEST_DIRECTORY_PATH)
