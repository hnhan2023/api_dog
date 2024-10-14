import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a test database (SQLite in-memory database for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override to use the test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database and tables for testing
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

def test_import_breeds(test_client):
    response = test_client.post("/import-breeds/")
    assert response.status_code == 200
    assert response.json()["message"] == "The breeds have been successfully imported."

def test_get_all_breeds(test_client):
    response = test_client.get("/breeds/")
    assert response.status_code == 200
    breeds = response.json()
    assert len(breeds) >= 1 

def test_get_breed_detail_by_name(test_client):
    response = test_client.get("/breeds/Affenpinscher/")
    assert response.status_code == 200
    breed = response.json()
    assert breed["name"] == "Affenpinscher"

def test_upload_image_for_breed(test_client):
    breed_name = "Affenpinscher"
    with open("test_image.jpg", "rb") as file:
        response = test_client.post(f"/breeds/{breed_name}/upload-image/", files={"file": file})
    assert response.status_code == 200
    assert response.json()["message"] == "Image uploaded successfully"

def test_delete_most_recent_image(test_client):
    breed_name = "Affenpinscher"
    response = test_client.delete(f"/breeds/{breed_name}/delete-image/")
    assert response.status_code == 200
    assert response.json()["message"] == "Most recent image deleted successfully"
