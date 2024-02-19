import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = [os.getenv('API_KEY0'), os.getenv('API_KEY1')]

cur = 0

def get_api_key():
    global cur
    cur = (1-cur)
    return GOOGLE_API_KEY[cur]