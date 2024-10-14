import os
import requests
from dotenv import load_dotenv


load_dotenv()
DOG_API_KEY = os.getenv("DOG_API_KEY")
# Récupérer les races de chiens depuis l'API
def fetch_dog_breeds():
    api_url = "https://api.thedogapi.com/v1/breeds"
    headers = {'x-api-key': DOG_API_KEY}
    params = {
        "limit": 10,  # Limiter les résultats à 10 races par page
        "page": 0     # Première page (page 0)
    }   
    response = requests.get(api_url, headers=headers, params=params)
    return response.json()

def fetch_dog_breed_detail(breed_id):
    api_url = f"https://api.thedogapi.com/v1/breeds/{breed_id}"
    headers = {'x-api-key': DOG_API_KEY}
    response = requests.get(api_url, headers=headers)
    return response.json()
