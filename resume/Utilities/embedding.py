import numpy as np
import google.generativeai as genai
from resume.Utilities.apikey import get_api_key
from sklearn.metrics.pairwise import cosine_similarity


GOOGLE_API_KEY = get_api_key()
genai.configure(api_key=GOOGLE_API_KEY)

def similarity_score(project_text, jd_text):
    result1 = genai.embed_content(
        model = 'models/embedding-001',
        content = project_text)

    embedding1 = np.array(result1['embedding']).reshape(1, -1)

    result2 = genai.embed_content(
        model = 'models/embedding-001',
        content = jd_text)

    embedding2 = np.array(result2['embedding']).reshape(1, -1)

    similarity = cosine_similarity(embedding1, embedding2)[0][0]

    return similarity*5