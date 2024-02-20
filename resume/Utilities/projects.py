from resume.Utilities.gemini import gemini_response


def get_projects(text):
    text = "extracted text from resume:\n" + text
    query = "\n\nProblem Statement: I had some resumes in pdf format from which I extracted text using pypdf2 library. Extracted text contains all the details written in resumes. we have to extract projects from it.\nApproach: We will find the Project section in the resume and extract out text from that section only. There will be section in the resume, named Projects or Key Projects or something like that. we will find all the projects in that section. Extract the data in json format.\nMost importantly the projects should be only from the text provided above, don't add anything from gemini side. Don't use synonymous words to replace words from text in the resume.\nThe data json format should have is given ahead. \nProjects\nEach project should have following things\n— project_title (title of the project)\n— short_description (short description of the project upto 30 words)\n— tech_stack (technologies used in the project)\n— time_duration (Tenure of the project)\ntime duration should have following things\n— start (start time of the project. format should be MM-YYYY)\n— end (end time of the project. format should be MM-YYYY)\n— duration_months (duration of the project. should be in months.)\n\nwhere ever tech_stack is not present in resume, just write string = \"null\" \nDon't consider work experience section for extracting projects data.\n"

    try:
      response = gemini_response(text+query)
      return response
    except Exception as e:
      return e
