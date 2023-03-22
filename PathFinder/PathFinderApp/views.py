from django.shortcuts import render
from django.http import HttpResponse
import openai
import os


def index(req):
    return HttpResponse("Hello, world. You're at the pathfinderapp index.")
# Create your views here.


api_key = os.environ.get('OPENAI_API_KEY', None)
print(api_key)


def chatbot(req):
    gpt_response = None

    if api_key is not None and req.method == 'POST':
        openai.api_key = api_key
        user_in = req.POST.get('user_input')
        prompt = user_in

        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.9,
            max_tokens=512,
        )
        print(response)
        print("salam")
        print(type(req))

    return render(req, 'chatgpt.html', {})
