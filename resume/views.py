import os
from django.shortcuts import render
from django.http import JsonResponse
# import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, 'index.html')



def generate(request):

    return JsonResponse({'API_KEY': os.getenv('API_KEY0')})

    # if request.method != 'POST':
    #     return JsonResponse({'output_text': 'not post method'})
    
    # if 'input_text' not in request.POST:
    #     return JsonResponse({'output_text': 'no input_text key in request.POST'})

    # GOOGLE_API_KEY = os.getenv('API_KEY0')
    # genai.configure(api_key=GOOGLE_API_KEY)
    # generation_config = {
    #     "temperature": 0,
    #     "top_p": 1,
    #     "top_k": 45,
    #     "max_output_tokens": 4096,
    # }
    # model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    # input_text = request.POST.get('input_text')
    
    # output_text = model.generate_content(input_text)
    # output_text.resolve()
    # return JsonResponse({'output_text': output_text.text})