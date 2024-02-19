import os
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, 'index.html')



def generate(request):

    GOOGLE_API_KEY = os.getenv('API_KEY0')
    genai.configure(api_key=GOOGLE_API_KEY)
    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 45,
        "max_output_tokens": 4096,
    }
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

    # return JsonResponse({'API_KEY': os.getenv('API_KEY0')})

    input_text = "I am a software developer and I have worked on many projects. I have worked on a project named 'Project1' and another project named 'Project2'. I have used technologies like Python, Django, and React in my projects. I have worked on these projects from 2020 to 2021. I have also worked on a project named 'Project3' and used technologies like Java, Spring, and Hibernate in it. I have worked on this project from 2019 to 2020."

    output_text = model.generate_content(input_text)
    output_text.resolve()
    return JsonResponse({'output_text': output_text.text})

    # if request.method != 'POST':
    #     return JsonResponse({'output_text': 'not post method'})
    
    # if 'input_text' not in request.POST:
    #     return JsonResponse({'output_text': 'no input_text key in request.POST'})

    # input_text = request.POST.get('input_text')
    