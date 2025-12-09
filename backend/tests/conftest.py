import pytest
from app import create_app

@pytest.fixture
def app(tmp_path):
    app = create_app()
    upload_folder = tmp_path / "test_uploads"
    upload_folder.mkdir()
    app.config.update({
        "TESTING": True,
        "UPLOADED_FILES": str(upload_folder)
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
