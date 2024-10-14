# Project Documentation: Dog Breeds API

## Table of Contents
1. [Project Overview](#project-overview)
2. [Candidate's Approach](#candidates-approach)

## Project Overview

This project is an API built using **FastAPI** that allows users to manage dog breeds and their associated images. The core functionalities include:
- Importing dog breeds from an external API and saving them in a database.
- Uploading images for specific breeds.
- Retrieving breed details and images.
- Displaying images via the API.
- Providing a random list of images.

## Candidate's Approach

### 1. **Architecture & File Structure**
The project is structured to maintain **separation of concerns**, keeping the code modular and clean. The core logic for handling the application is divided into services, routes, and models, with utility functions where appropriate.

#### File Structure
```plaintext
my-dog-api/
├── app/
│   ├── __init__.py            # Package initialization
│   ├── models.py              # Database models (Breed, Image)
│   ├── routes.py              # API routes and endpoints
│   ├── services.py            # Business logic for breeds and images
│   ├── utils.py               # Utility functions
│   ├── database.py            # SQLAlchemy/PostgreSQL configuration
│   └── config.py              # Configuration (API keys, DB settings)
├── uploads/                   # Images uploaded by user via the api
├── tests/                     # Unit tests
├── README.md                  # Project documentation
```

### 2. API Functionality

- **/import-breeds/** (POST): Imports dog breeds from [The Dog API](https://thedogapi.com/) and stores them in the database.

- **/breeds/** (GET):  Retrieve all dog breeds from the database.

- **/breeds/{breed_name}/** (GET):  Retrieve breed details by breed name.
  
- **/breeds/{breed_name}/upload-image/** (POST): Allows users to upload an image for a specific breed. The uploaded images are stored on the server, and their file paths are saved in the database.
  
- **/breeds/{breed_name}/display/** (GET): Displays the most recent image of a specific breed in the browser.

- **/images/{image_id}/display/** (GET): Retrieves an image by its ID and serves it in the browser.

- **/breeds/images/random-list/** (GET): Retrieves a random list of 20 images (or any specified limit) with their respective URLs.

- **/breeds/{breed_name}/delete-image/** (DELETE): Deletes the most recent image associated with a specific breed.

---

### 3. Services & Utilities

**Services**: Business logic has been moved to service functions to maintain clean route handlers.

- Manage the business logic for image uploads, deletions, and breed imports.

**Utilities**: Utility functions handle repetitive tasks like file handling and URL construction.

- Handle common tasks such as file path generation and image URL construction.

---

### 4. Database Models

- **Breed Model**: Stores breed details, including name, life span, and breed group.
- **Image Model**: Stores image file paths associated with breeds. Each breed can have multiple images.

---

### 5. Error Handling

Comprehensive error handling has been implemented for all routes:

- If a breed or image is not found, appropriate HTTP status codes (e.g., 404) are returned with descriptive error messages.

---

### 6. Potential Improvements

1. **Pagination Support**: 
   - Currently, the API returns random lists of images with a limit parameter. Adding pagination support for large datasets would enhance performance and usability.

2. **Advanced Breed Filtering**: 
   - Currently, breeds can be queried only by name. Adding filters such as breed group, life span, and size could improve user experience.

3. **Cloud Storage for Images**: 
   - Instead of storing images locally, integrating with cloud storage services (e.g., AWS S3 or Google Cloud Storage) would improve scalability, especially for large datasets.

4. **User Authentication**:
   - Adding authentication and authorization (e.g., JWT or OAuth) would restrict access to certain routes (e.g., image uploads and deletions).

5. **Image Optimization**:
   - Adding functionality to resize or compress images upon upload would save server storage and reduce image load times.

6. **Rate Limiting**:
   - Adding rate limiting to the API (e.g., for image uploads) could prevent abuse and enhance security.


---

### 7. Useful Information

#### External API:

- The breeds are imported from [The Dog API](https://thedogapi.com/). An API key is required, which must be configured in the environment variables (`DOG_API_KEY`).

#### Database:

- **PostgreSQL** is used to store breed and image data. The database connection string should be configured in the `.env` file.

#### Running the API Locally:

- When running locally, images are served from the server's local file system. Ensure the image directory is writable and accessible.

#### Base URL for Images:

- Image URLs are constructed using the base URL defined in the configuration file. In production, this should be updated to the actual domain where the app is hosted.

#### Error Handling:

- All API routes have comprehensive error handling, with appropriate HTTP response codes and messages for various scenarios, such as missing breeds or images.