from PyPDF2 import PdfReader
from django.shortcuts import render
from django.http import JsonResponse
from resume.Utilities.projects import get_projects
from resume.Utilities.score import similarity_score
from resume.Utilities.embedding import get_embedding
from resume.Utilities.education import get_education
from resume.Utilities.intro import get_name, get_email
from resume.Utilities.workex import get_work_experiences


ret = []
poll_data = []
threshold_value_for_resume_selection = 0.0


def index(request):
    return render(request, 'index.html')


def generate(request):

    if request.method == 'POST':


        jd_text = "Job Description:\n"
        if 'jobDescription' in request.POST:
            jd_text += request.POST.get('jobDescription')
        jd_text_embedding = get_embedding(jd_text)


        if request.FILES and "resume" in request.FILES:
            global ret
            res = []
            pdf_files = request.FILES.getlist("resume")
            for index, pdf_file in enumerate(pdf_files):
                text = ""
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()


                name = get_name(text)
                email = get_email(text)

                details = {}
                finaltext = []

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
                        finaltext.append((score, imp_text))
                    projects['Projects'].sort(key=lambda x: x['relevancy'], reverse=True)
                    details['projects'] = projects['Projects']
                except Exception as e:
                    print("Error in projects section: ", e)


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
                        finaltext.append((score, imp_text))
                    work_experiences['Professional Experience'].sort(key=lambda x: x['relevancy'], reverse=True)
                    details['Professional Experience'] = work_experiences['Professional Experience']
                except Exception as e:
                    print("Error in work_experience section: ", e)


                try:
                    education = get_education(text)
                    details['education'] = education['College']
                except Exception as e:
                    print("Error in education: ", e)


                # print(details)


                imp_project_workex=""
                finaltext.sort(key=lambda x: x[0], reverse=True)
                for i in range(min(3, len(finaltext))):
                    imp_project_workex += finaltext[i][1]
                overall_embedding = get_embedding(imp_project_workex)
                overall_score = similarity_score(overall_embedding, jd_text_embedding)
                overall_score = round(overall_score, 2)


                if overall_score >= threshold_value_for_resume_selection:
                    ret.append({'name': name, "email": email, "score": overall_score, 'resume_index': str(index), 'details': details})
                    res.append({'name': name, "email": email, "score": overall_score, 'resume_index': str(index), 'details': details})

                # print(ret)

            return JsonResponse(res, safe=False)
        else:
            return JsonResponse({'error': 'No PDF files found in the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)



def poll(request):
    global ret
    poll_data = ret
    ret = []
    return JsonResponse(poll_data, safe=False)