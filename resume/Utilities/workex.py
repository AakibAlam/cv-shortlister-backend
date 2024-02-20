from resume.Utilities.gemini import gemini_response


def get_work_experiences(text):
    text = "extracted text from resume:\n" + text
    query = "\n\nProblem Statement: I had some resumes in pdf format from which I extracted text using pypdf2 library. Extracted text contains all the details written in resumes. we have to extract work experience from it.\nApproach: We will find the work experience section in the resume and extract out text from that section only. There will be section in the resume, named Work experience or Professional experience or something like that. we will find all the work experience in that section. Extract the data in json format.\nMost importantly the work experience should be only from the text provided above, don't add anything from gemini side. Don't use synonymous words to replace words from text in the resume.\nThe data json format should have is given ahead. \nProfessional Experience\nEach work experience should have following things\n— role (Designation)\n- Organization\n— short_description (short description of work done upto 30 words)\n— tech_stack (technologies used in the work)\n— time_duration (Tenure of the professional experience)\ntime duration should have following things\n— start (start time of the work. format should be MM-YYYY)\n— end (end time of the work. format should be MM-YYYY)\n— duration_months (duration of the project. should be in months.)\n\nwhere ever tech_stack is not present in resume, just write string = \"null\" \nDon't consider projects section for extracting work experience data.\n"

    try:
      response = gemini_response(text+query)
      return response
    except Exception as e:
      return e