from huggingface_hub import login
import os
from dotenv import load_dotenv 

load_dotenv()

access_token = os.getenv("HUGGING_FACE_TOKEN")

def login_huggingface():    
    login(token = access_token)

    