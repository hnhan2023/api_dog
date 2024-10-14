import pytest
from sqlalchemy.orm import Session
from app.services import (
    import_breeds_to_db, 
    get_all_breeds_service, 
    get_breed_details_service, 
    upload_image_service,
    delete_most_recent_image_service
)
from app.models import Breed, Image
from fastapi import UploadFile
from io import BytesIO

@pytest.fixture
def test_db_session():
    """Provides a test session for each test."""
    # Set up the in-memory database for tests
    from app.database import get_db, engine, Base
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()

def test_import_breeds_to_db(test_db_session):
    """Test breed import service"""
    result = import_breeds_to_db(test_db_session)
    breeds = test_db_session.query(Breed).all()
    assert len(breeds) > 0  # Ensure that breeds are imported

def test_get_all_breeds_service(test_db_session):
    """Test get all breeds service"""
    breeds = get_all_breeds_service(test_db_session)
    assert len(breeds) > 0  # Ensure breeds are retrieved

def test_get_breed_details_service(test_db_session):
    """Test breed detail retrieval service"""
    breed_name = "Affenpinscher"
    breed = get_breed_details_service(breed_name, test_db_session)
    assert breed.name == breed_name

@pytest.mark.asyncio
async def test_upload_image_service(test_db_session):
    """Test uploading an image for a breed"""
    breed_name = "Affenpinscher"
    file_content = BytesIO(b"test image content")
    file = UploadFile(filename="test_image.jpg", file=file_content)
    result = await upload_image_service(breed_name, file, test_db_session)
    assert result["message"] == "Image uploaded successfully"

def test_delete_most_recent_image_service(test_db_session):
    """Test deleting the most recent image"""
    breed_name = "Affenpinscher"
    result = delete_most_recent_image_service(breed_name, test_db_session)
    assert result["message"] == "Most recent image deleted successfully"