import json
import google.generativeai as genai
from resume.Utilities.apikey import get_api_key


GOOGLE_API_KEY = get_api_key()
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 45,
  "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)


def get_education(text):
    text = "extracted text from resume:\n" + text
    query = "\n\nProblem Statement: I had some resumes in pdf format from which I extracted text using pypdf2 library. Extracted text contains all the details written in resumes. we have to extract Educational Qualification from it.\nApproach: We will find the Education section in the resume and extract out text from that section only. There will be section in the resume, named Educational Qualification or Education or something like that. we will find all the degree from that section. Extract the data in json format.\nMost importantly the projects should be only from the text provided above, don't add anything from gemini side. Don't use synonymous words to replace words from text in the resume.\nThe data json format should have is given ahead. \nCollege\nEach degree should have following things\n— name (name of the college for the given candidate)\n— branch (the branch of the candidate in college)\n— degree (degree of the candidate for the enrolment)\n— cgpa (latest cgpa/cpi of the candidate)\n— start (enrolment time in the college for the candidate. format should be MM-YYYY)\n— end (graduation month for the candidate. format should be MM-YYYY)\n— duration_months (duration of the project. should be in months.)\n\nwhichever field is not present in the text, just write string = \"null\" \n"

    response = model.generate_content(text+query)
    response.resolve()

    response = response.text.strip('`')
    start_index = response.find("{")
    json_content = response[start_index:]
    try:
      education = json.loads(json_content)
      return education
    except json.JSONDecodeError as e:
      print("Error decoding JSON:", e)
      return None
