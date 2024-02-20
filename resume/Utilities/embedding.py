import os
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def get_embedding(text):
    try:
        response = genai.embed_content(
            model='models/embedding-001',
            content=text
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    embedding = np.array(response['embedding']).reshape(1, -1)

    return embedding