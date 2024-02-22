from PyPDF2 import PdfReader
from django.shortcuts import render
from django.http import JsonResponse
from resume.Utilities.projects import get_projects
from resume.Utilities.score import similarity_score
from resume.Utilities.embedding import get_embedding
from resume.Utilities.education import get_education
from resume.Utilities.intro import get_name, get_email
from resume.Utilities.workex import get_work_experiences
import concurrent.futures

ret = []
threshold_value_for_resume_selection = 0.0


def index(request):
    return render(request, 'index.html')



def process_projects(text, jd_text_embedding):
    try:
        projects = get_projects(text)
        for project in projects['Projects']:
            desc = project['short_description']
            techs = project['tech_stack']
            imp_text = "\n" # to avoid empty string
            if desc is not None:
                imp_text += desc
            if techs is not None:
                imp_text += techs
            imp_text_embedding = get_embedding(imp_text)
            score = similarity_score(imp_text_embedding, jd_text_embedding)
            project['relevancy'] = score
        projects['Projects'].sort(key=lambda x: x['relevancy'], reverse=True)
        return projects
    except Exception as e:
        print("Error in projects section: ", e)



def process_workex(text, jd_text_embedding):
    try:
        work_experiences = get_work_experiences(text)
        for work_experience in work_experiences['Professional Experience']:
            desc = work_experience['short_description']
            techs = work_experience['tech_stack']
            imp_text = "\n" # to avoid empty string
            if desc is not None:
                imp_text += desc
            if techs is not None:
                imp_text += techs
            imp_text_embedding = get_embedding(imp_text)
            score = similarity_score(imp_text_embedding, jd_text_embedding)
            work_experience['relevancy'] = score
        work_experiences['Professional Experience'].sort(key=lambda x: x['relevancy'], reverse=True)
        return work_experiences
    except Exception as e:
        print("Error in work_experience section: ", e)



def process_education(text):
    try:
        education = get_education(text)
        return education
    except Exception as e:
        print("Error in education: ", e)



def process_resume(text, jd_text_embedding, index):

    resume_content = {}
    resume_content['resume_index'] = index
    name = get_name(text)
    resume_content['name'] = name
    email = get_email(text)
    resume_content['email'] = email

    details = {}
    finaltext = []

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures.append(executor.submit(process_projects, text, jd_text_embedding))
        futures.append(executor.submit(process_workex, text, jd_text_embedding))
        futures.append(executor.submit(process_education, text))

    results = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        # print("result: ", result)
        if 'Projects' in result:
            details['Projects'] = result['Projects']
            for project in details['Projects']:
                finaltext.append((project['relevancy'], project['short_description']+project['tech_stack']))
        elif 'Professional Experience' in result:
            details['Professional Experience'] = result['Professional Experience']
            for work_experience in details['Professional Experience']:
                finaltext.append((work_experience['relevancy'], work_experience['short_description']+work_experience['tech_stack']))
        elif 'Education' in result:
            details['Education'] = result['Education']

    resume_content['details'] = details
    # print("details: ", details)

    imp_project_workex=""
    finaltext.sort(key=lambda x: x[0], reverse=True)
    for i in range(min(3, len(finaltext))):
        imp_project_workex += finaltext[i][1]
    overall_embedding = get_embedding(imp_project_workex)
    overall_score = similarity_score(overall_embedding, jd_text_embedding)
    overall_score = round(overall_score, 2)
    resume_content['score'] = overall_score


    return resume_content



def generate(request):
    if request.method == 'POST':
        jd_text = "Job Description:\n"
        if 'jobDescription' in request.POST:
            jd_text += request.POST.get('jobDescription')
        jd_text_embedding = get_embedding(jd_text)

        if request.FILES and "resume" in request.FILES:
            pdf_files = request.FILES.getlist("resume")

            global ret
            results = []
            for index, pdf_file in enumerate(pdf_files):
                content = process_pdf(pdf_file, jd_text_embedding, index)
                if (content['score'] > threshold_value_for_resume_selection):
                    ret.append(content)
                    results.append(content)

            return JsonResponse(results, safe=False)
        else:
            return JsonResponse({'error': 'No PDF files found in the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)



def process_pdf(pdf_file, jd_text_embedding, index):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()

    return process_resume(text, jd_text_embedding, index)



def poll(request):
    global ret
    poll_data = ret
    ret = []
    return JsonResponse(poll_data, safe=False)

