from django.shortcuts import render
from django.http import HttpResponse
import openai
import os


api_key = os.environ.get(
    'OPENAI_API_KEY', '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')
print(api_key)
# Create your views here.


def chatbot(chat_query_request):
    if api_key is not None and chat_query_request.method == 'POST':
        openai.api_key = api_key
        user_in = chat_query_request.POST.get('query')
        prompt = user_in
        # promptt = f""
        print(prompt)

        full_api_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=512,

        )
        gpt_response = ''
        print(full_api_response)
        print(type(chat_query_request))
        gpt_response = full_api_response['choices'][0]['text']

    return render(chat_query_request, 'chatgpt.html', {'response': gpt_response})
