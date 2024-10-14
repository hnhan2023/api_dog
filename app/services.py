from http.client import HTTPException
import os
import requests
from dog_api.app.models.image import Image
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from datetime import datetime
from app.models import Breed
from app.utils import fetch_dog_breed_detail, fetch_dog_breeds
from fastapi.responses import FileResponse
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
BASE_IMAGE_URL = os.getenv("BASE_IMAGE_URL")


def import_breeds_to_db(db: Session):
    breeds_data = fetch_dog_breeds()
    races_importees = 0
    for breed in breeds_data:
        breed_details = fetch_dog_breed_detail(breed['id'])
        if db.query(Breed).filter(Breed.name == breed_details['name']).first():
            continue
        new_breed = Breed(
            id=breed_details['id'],
            name=breed_details['name'],
            weight=breed_details.get('weight', ''),
            height=breed_details.get('height', ''),
            life_span=breed_details.get('life_span', ''),
            bred_for=breed_details.get('bred_for', ''),
            breed_group=breed_details.get('breed_group', '')
        )
        db.add(new_breed)
        db.commit()    
    return races_importees

def get_all_breeds_service(db: Session):
    breeds = db.query(Breed).all()
    if not breeds:
        raise {"error": "No Breed founded"}
    return breeds

    
def get_breed_details_service(breed_name: str, db: Session):
    breed = db.query(Breed).filter(Breed.name == breed_name).first()
    if not breed:
        return {"error": "Breed not found"}
    return breed

async def upload_image_service(breed_name: str, file: UploadFile, db: Session):
    try:
        breed = db.query(Breed).filter(Breed.name == breed_name).first()
        if not breed:
            raise HTTPException(status_code=404, detail="Breed not found")
        #Get the file extension of the uploaded file
        _, file_extension = os.path.splitext(file.filename)
        #Create the file name based on the breed name
        sanitized_breed_name = breed_name.replace(" ", "_").lower()
        file_time = datetime.utcnow()
        file_name = f"{sanitized_breed_name}_{file_time.strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        #Save the image to the server
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        new_image = Image(
            image_path=file_path,
            breed_id=breed.id,
            created_at=file_time
        )
        db.add(new_image)
        db.commit()
        return {"message": "Image uploaded successfully", "image_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
    
def delete_most_recent_image_service(breed_name: str, db: Session):
    """
    Service to delete the most recent image for a specific breed.
    """
    try:
        breed = db.query(Breed).filter(Breed.name == breed_name).first()
        if not breed:
            raise HTTPException(status_code=404, detail="Breed not found")
        # Find the most recent image for the breed
        image = db.query(Image).filter(Image.breed_id == breed.id).order_by(Image.created_at.desc()).first()
        if not image:
            raise HTTPException(status_code=404, detail="No images found for this breed")
        if os.path.exists(image.image_path):
            os.remove(image.image_path)
        db.delete(image)
        db.commit()
        return {"message": "Most recent image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")
    
def get_image_by_id_service(image_id: int, db: Session):
    """
    Service to get an image by its ID and serve it for display.
    """
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        if not os.path.exists(image.image_path):
            raise HTTPException(status_code=404, detail="Image file not found on the server")
        return FileResponse(image.image_path, media_type='image/jpeg')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to display image: {str(e)}")
    
def display_last_image_by_breed_service(breed_name: str, db: Session):
    """
    Service to find the most recent image for a specific breed and return it for display.
    """
    try:
        breed = db.query(Breed).filter(Breed.name == breed_name).first()
        if not breed:
            raise HTTPException(status_code=404, detail="Breed not found")
        image = db.query(Image).filter(Image.breed_id == breed.id).order_by(Image.created_at.desc()).first()
        if not image:
            raise HTTPException(status_code=404, detail="No images found for this breed")
        if not os.path.exists(image.image_path):
            raise HTTPException(status_code=404, detail="Image file not found on the server")
        return FileResponse(image.image_path, media_type='image/jpeg')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to display the image: {str(e)}")
    
def get_random_images_service(limit: int, db: Session):
    """
    Service to retrieve a random list of images with a dynamic limit.
    """
    try:
        random_images = db.query(Image).order_by(func.random()).limit(limit).all()

        if not random_images:
            raise HTTPException(status_code=404, detail="No images available")
        image_urls = [f"{BASE_IMAGE_URL}{image.id}" for image in random_images]

        return {"images": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve random images: {str(e)}")