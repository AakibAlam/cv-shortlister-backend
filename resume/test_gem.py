import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY0')
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 45,
  "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

def get_projects(text):
    text = "extracted text from resume:\n" + text
    query = "\n\nProblem Statement: I had some resumes in pdf format from which I extracted text using pypdf2 library. Extracted text contains all the details written in resumes. we have to extract projects from it.\nApproach: We will find the Project section in the resume and extract out text from that section only. There will be section in the resume, named Projects or Key Projects or something like that. we will find all the projects in that section. Extract the data in json format.\nMost importantly the projects should be only from the text provided above, don't add anything from gemini side. Don't use synonymous words to replace words from text in the resume.\nThe data json format should have is given ahead. \nProjects\nEach project should have following things\n— project_title (title of the project)\n— short_description (short description of the project upto 30 words)\n— tech_stack (technologies used in the project)\n— time_duration (Tenure of the project)\ntime duration should have following things\n— start (start time of the project. format should be MM-YYYY)\n— end (end time of the project. format should be MM-YYYY)\n— duration_months (duration of the project. should be in months.)\n\nwhere ever tech_stack is not present in resume, just write string = \"null\" \nDon't consider work experience section for extracting projects data.\n"

    response = model.generate_content(text+query)
    response.resolve()
    # print(response.text)
    response = response.text.strip('`')
    start_index = response.find("{")
    json_content = response[start_index:]
    try:
      projects = json.loads(json_content)
      return projects
    except json.JSONDecodeError as e:
      print("Error decoding JSON:", e)
      return None


print(get_projects("I am a software developer and I have worked on many projects. I have worked on a project named 'Project1' and another project named 'Project2'. I have used technologies like Python, Django, and React in my projects. I have worked on these projects from 2020 to 2021. I have also worked on a project named 'Project3' and used technologies like Java, Spring, and Hibernate in it. I have worked on this project from 2019 to 2020."))