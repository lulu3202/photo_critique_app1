import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
if api_key:
    print("API Key Loaded Successfully!")
else:
    print("Failed to Load API Key.")
