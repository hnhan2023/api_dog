import os
from dotenv import load_dotenv

load_dotenv()

DOG_API_KEY = os.getenv("DOG_API_KEY")
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
BASE_IMAGE_URL = os.getenv("BASE_IMAGE_URL")