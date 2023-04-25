from django.shortcuts import render
from django.http import JsonResponse
import os
import json
import pickle, warnings
import openai
import pinecone
import PathFinder.PathFinderModels.pathfinder_chat_bot as qamodel
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from .forms import ChatBotForm

api_key = os.environ.get('OPENAI_API_KEY')

# warnings.filterwarnings("ignore")

def qachain(request):

    # qamodel.load_embed_pickle()
    pinecone.init(api_key='5bf2927b-0fb7-423b-b8f1-2f6a3347a15d',
                environment='asia-northeast1-gcp')
    vectorstore = Pinecone.from_existing_index('teamprojindex', OpenAIEmbeddings())
    pathfinder_chatbot = qamodel.make_chain(vectorstore)
    chat_history = []
    # print(vectorstore.similarity_search("what is a computer", 10))
    question = input("Enter a question: ")

    # answer = pathfinder_chatbot({
    #     "question": question,
    #     "chat_history": []
    # })
    # print(answer)
    # print(chatbot.)
    while 1:
        answer = pathfinder_chatbot({
            "question": question,
            "chat_history": chat_history
        })
        print()
        print(answer)
        chat_history.append({"role": "assistant", "content": answer})
        print('type exit to exit...')
        question = input()
        if question == "exit":
            break

    # with open("ndtmvecstore.pkl", "rb") as f:
    #     vectorstore = pickle.load(f)
    #     print(qamodel.make_chain_prebuilt(vectorstore))

    return 0
# qachain(None)
def test_chatbotview(request):
    pinecone.init(api_key='5bf2927b-0fb7-423b-b8f1-2f6a3347a15d',
                environment='asia-northeast1-gcp')
    vectorstore = Pinecone.from_existing_index('teamprojindex', OpenAIEmbeddings())
    pathfinder_chatbot = qamodel.make_chain(vectorstore)

    if request.method == 'POST':
        form = ChatBotForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            response = pathfinder_chatbot({
                "question": message,
                "name": name,
                "chat_history": []
            }) # query the chatbot
            return JsonResponse({'response': response})
    else:
        form = ChatBotForm(request.POST)
    return render(request, 'chatbox.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def gdpr(request):
    return render(request, 'gdpr.html')

def about(request):
    return render(request, 'about.html')

def chatwindow(request):
    return render(request, 'chatwindow.html')


def chatbot(chat_query_response):
    openai.api_key = api_key
    gpt_response = ''
    prompt="Welcome the user and ask them what they want to learn about."

    chat_history = [
        {"role": "system",
            "content": "You are PathFinder, ChatGPTs distant cousin trained by us (an unknown entity). Answer as informatively and academically as possible"},
        {"role": "assistant", "content": "I am a chatbot, I am here to help you"},
        {"role": "assistant", "content": "I will answer questions about academic subjects"},
    ]
    if api_key is not None and chat_query_response.method == 'POST':
        user_in = chat_query_response.POST.get('query')
        prompt = user_in
        # print('api key')
    else:
        print("No API key set, please set one in the environment variable OPENAI_API_KEY")

        # User msgs below help instruct the 'assistant' aka the GPT model.
        # can be developer set instructs and user set >>> work can be done here regarding tweaking the model to our applications needs.
        # print(prompt)

        # chat history will probably have to be taken care of with js and eventually probably persisted in a db.
    if prompt is not None:
        chat_history.append({"role": "user", "content": prompt})
        full_api_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens=2048,
        )
        gpt_response = full_api_response.choices[0].message.content
    # print(full_api_response)
    # print(chat_history)
    chat_history.append({"role": "assistant", "content": gpt_response})
    return render(chat_query_response, 'chatgpt.html', {'response': gpt_response})
    # print(full_api_response)
    # print(type(chat_query_response))

# m = openai.Model.list()
# print([m['id'] for m in m['data'] if m['id'].startswith('gpt')])
# models= list(openai.Model.list().values())[1]
# print(models)
# print(list(filter(lambda x: re.match('*gpt*', x) , models)))


# *ASIDE: Function for token counting queries.

# def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
#   try:
#       encoding = tiktoken.encoding_for_model(model)
#   except KeyError:
#       encoding = tiktoken.get_encoding("cl100k_base")
#   if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
#       num_tokens = 0
#       for message in messages:
#           num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
#           for key, value in message.items():
#               num_tokens += len(encoding.encode(value))
#               if key == "name":  # if there's a name, the role is omitted
#                   num_tokens += -1  # role is always required and always 1 token
#       num_tokens += 2  # every reply is primed with <im_start>assistant
#       return num_tokens
#   else:
#       raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
#   See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")