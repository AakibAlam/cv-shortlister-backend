import json
from resume.Utilities.apikey import get_api_key
import google.generativeai as genai

GOOGLE_API_KEY = get_api_key()
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 45,
    "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

def get_work_experiences(text):
    text = "extracted text from resume:\n" + text
    query = "\n\nProblem Statement: I had some resumes in pdf format from which I extracted text using pypdf2 library. Extracted text contains all the details written in resumes. we have to extract work experience from it.\nApproach: We will find the work experience section in the resume and extract out text from that section only. There will be section in the resume, named Work experience or Professional experience or something like that. we will find all the work experience in that section. Extract the data in json format.\nMost importantly the work experience should be only from the text provided above, don't add anything from gemini side. Don't use synonymous words to replace words from text in the resume.\nThe data json format should have is given ahead. \nProfessional Experience\nEach work experience should have following things\n— role (Designation)\n- Organization\n— short_description (short description of work done upto 30 words)\n— tech_stack (technologies used in the work)\n— time_duration (Tenure of the professional experience)\ntime duration should have following things\n— start (start time of the work. format should be MM-YYYY)\n— end (end time of the work. format should be MM-YYYY)\n— duration_months (duration of the project. should be in months.)\n\nwhere ever tech_stack is not present in resume, just write string = \"null\" \nDon't consider projects section for extracting work experience data.\n"

    response = model.generate_content(text+query)
    response.resolve()
    # print(response.text)
    response = response.text.strip('`')
    start_index = response.find("{")
    json_content = response[start_index:]
    try:
      work_experience = json.loads(json_content)
      return work_experience
    except json.JSONDecodeError as e:
      print("Error decoding JSON:", e)
      return None