from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.services import delete_most_recent_image_service, display_last_image_by_breed_service, get_all_breeds_service, get_breed_details_service, get_image_by_id_service, get_random_images_service, import_breeds_to_db, upload_image_service
from app.database import get_db

router = APIRouter()

@router.post("/import-breeds/")
def import_breeds(db: Session = Depends(get_db)):
    """
    Imports dog breeds from an external API and stores them in the database.
    USER STORY: All the user stories below are expected to be requested through a REST API.
    """
    try:
        # Appel à la fonction d'import des races
        import_breeds_to_db(db)
        
        # Message de succès après importation
        return {"message": "The breeds have been successfully imported."}
    
    except Exception as e:
        # Gestion des erreurs générales
        raise HTTPException(status_code=500, detail=f"Failed to import breeds: {str(e)}")

@router.get("/breeds/")
def get_all_breeds(db: Session = Depends(get_db)):
    """
    Retrieve all dog breeds from the database.
    USER STORY: As a user, I want to retrieve all breeds.
    """
    try:
        return get_all_breeds_service(db)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve breed: {str(e)}")

    
@router.get("/breeds/{breed_name}/")
def get_breed_detail_by_name(breed_name: str, db: Session = Depends(get_db)):
    """
    Retrieve breed details by breed name.
    USER STOTY: As a user, I want to retrieve information about a specific breed. 
    """
    try:
        return get_breed_details_service(breed_name, db)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve breed: {str(e)}")


@router.post("/breeds/{breed_name}/upload-image/")
async def upload_image(breed_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload an image for a specific breed by name.
    USER STOTY: As a user, I want to upload and attach an image to a specific breed (server-side upload). 
    """
    return await upload_image_service(breed_name, file, db)
    
 
@router.delete("/breeds/{breed_name}/delete-image/")
def delete_most_recent_image(breed_name: str, db: Session = Depends(get_db)):
    """
    Delete the most recent image for a specific breed.
    USER STOTY: As a user, I want to delete an image from a specific breed.
    """
    return delete_most_recent_image_service(breed_name, db)

@router.get("/images/{image_id}/display/")
def display_image_by_id(image_id: int, db: Session = Depends(get_db)):
    """
    Display an image by its ID.
    USER STOTY : As a user, I want to get any image previously uploaded. +  
    As a user, I want to display an image previously uploaded (e.g: must be visible through the browser).   
    """
    return get_image_by_id_service(image_id, db)

@router.get("/breeds/{breed_name}/display/")
def display_the_last_image_by_race(breed_name: str, db: Session = Depends(get_db)):
    """
    Display the most recent image for a specific breed by name.
    USER STOTY : As a user, I want to get any image previously uploaded. +  
    As a user, I want to display an image previously uploaded (e.g: must be visible through the browser).  
    """
    return display_last_image_by_breed_service(breed_name, db)
    
@router.get("/breeds/images/random-list/")
def get_random_images(limit: int = 20, db: Session = Depends(get_db)):
    """
    Retrieve a random list of images with a dynamic limit.
    USER STOTY: As a user, I want to retrieve a random list of 20 images with their respective URLs (dynamic counter is accepted).
    """
    return get_random_images_service(limit, db)
