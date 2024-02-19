import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from PyPDF2 import PdfReader
from resume.Utilities.apikey import get_api_key
from resume.Utilities.projects import get_projects
from resume.Utilities.education import get_education
from resume.Utilities.intro import get_name, get_email
from resume.Utilities.embedding import similarity_score
from resume.Utilities.workex import get_work_experiences
import google.generativeai as genai


threshold_value_for_resume_selection = 0.0


def index(request):
    return render(request, 'index.html')


def generate(request):

    if request.method == 'POST':
        jd_text = "Job Description:\n"
        if 'jobDescription' in request.POST:
            jd_text += request.POST.get('jobDescription')
        # print(jd_text)
        if request.FILES and "resume" in request.FILES:
            pdf_files = request.FILES.getlist("resume")
            ret = []
            details = {}
            for index, pdf_file in enumerate(pdf_files):
                text = ""
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()

                name = get_name(text)
                email = get_email(text)

                max_project_score=0
                projects = get_projects(text)
                if projects is not None and 'Projects' in projects:
                    for project in projects['Projects']:
                        desc = project['short_description']
                        techs = project['tech_stack']
                        imp_text = "\n" # to avoid empty string
                        if desc is not None:
                            imp_text += desc
                        if techs is not None:
                            imp_text += techs
                        score = similarity_score(imp_text, jd_text)
                        score = 1.0
                        project['relevancy'] = score
                        max_project_score = max(max_project_score, score)
                    projects['Projects'].sort(key=lambda x: x['relevancy'], reverse=True) 
                    details['projects'] = projects['Projects']


                

                max_work_score=0
                work_experiences = get_work_experiences(text)
                if work_experiences is not None and 'Professional Experience' in work_experiences:
                    for work_experience in work_experiences['Professional Experience']:
                        desc = work_experience['short_description']
                        techs = work_experience['tech_stack']
                        imp_text = "\n" # to avoid empty string
                        if desc is not None:
                            imp_text += desc
                        if techs is not None:
                            imp_text += techs
                        score = similarity_score(imp_text, jd_text)
                        work_experience['relevancy'] = score
                        max_work_score = max(max_work_score, score)
                    work_experiences['Professional Experience'].sort(key=lambda x: x['relevancy'], reverse=True)
                    details['Professional Experience'] = work_experiences['Professional Experience']


                details['education'] = None
                education = get_education(text)
                if education is not None and 'College' in education:
                    details['education'] = education['College']

                print(details)

                relevancy_score = (max_project_score + max_work_score) / 2
                relevancy_score = round(relevancy_score, 2)


                if relevancy_score >= threshold_value_for_resume_selection:
                    ret.append({'name': name, "email": email, "score": relevancy_score, 'resume_index': str(index), 'details': details})

            ret.sort(key=lambda x: x['score'], reverse=True)
            return JsonResponse(ret, safe=False)
        else:
            return JsonResponse({'error': 'No PDF files found in the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)