import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 45,
  "max_output_tokens": 4096,
}
model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)


def gemini_response(text):
    try:
      response = model.generate_content(text)
      response.resolve()
      response = response.text.strip('`')
      start_index = response.find("{")
      json_content = response[start_index:]
      json_response = json.loads(json_content)
      # print(json_response)
      return json_response
    except json.JSONDecodeError as e:
      return e