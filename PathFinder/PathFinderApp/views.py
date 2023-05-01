from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import PathFinder.PathFinderModels.pathfinder_chat_bot as qamodel
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from PathFinder.PathFinderApp.forms import RegisterUserForm, ChatBotForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import EditProfileForm,UpdateProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import os
import json
# import pickle
# import warnings
import openai
import pinecone


api_key = os.environ.get('OPENAI_API_KEY')

# warnings.filterwarnings("ignore")

pinecone.init(api_key='5bf2927b-0fb7-423b-b8f1-2f6a3347a15d',
              environment='asia-northeast1-gcp')
vectorstore = Pinecone.from_existing_index(
    'teamprojindex', OpenAIEmbeddings())
pathfinder_chatbot = qamodel.make_chain(vectorstore)

    # context = {
    #     'pathfinder_response':send_chat_response(request),
    #     'pathfinder_api_url': reverse('chatbox'),
    # }
    # request.session['pathfinder_response'] = send_chat_response(request)
    # send_chat_response(request)
    # if request.POST.get('user_message') not in [None, '']:
        # print("yes")

        # print(f"USERMSG INSIDE RENDERER: {request.POST.get('user_message')}")
    # print("hellop")
    # if request.POST.get('user_message'):
    #     send_chat_response(request)
    #     print("yes")

    # context = {
        # 'pathfinder_response': request.session['pathfinder_response'],
    # }

    # print(f"\ntypeof: {type(context['pathfinder_response'])}")

def render_chatbotview(request):
    # # print(request.POST)
    # print('ran')
    return render(request, 'chatwindow.html')

def send_chat_response(request):
    print(request.POST)
    pathfinder_response = ""
    # if user_message in [None, '']:
    #     # TODO: Obviously a temporary fix
    #     user_message = "The user is about to start a conversation with you, greet them and let them know what you can do."

    if request.method == 'POST':
        # user_message = request.POST.get('user_message')
        dat = json.loads(request.body)
        user_message = dat['user_message']
        print(type(user_message))
        # print("its allliiiivveee")
        print(f"USER_MESSAGE: {user_message}")
        # print(user_messaguser_message)
        # print('user_messaguser_message is not none')

        #! form = ChatBotForm(request.POST or None)
        if user_message is not None:
            response = pathfinder_chatbot({
                "question": user_message,
                # "name": name,
                "chat_history": []
            })  # query the chatbot
            # print(user_message)

            pathfinder_response = response['answer']
            # context = {'pathfinder_response': pathfinder_response}
        # jsondata = json.dumps(jsonresp)
    # reverse('/chatbox/')
    return JsonResponse({'pathfinder_response': pathfinder_response})
    # return JsonResponse({'pathfinder_response': pathfinder_response})
    # return render(request, 'chatwindow.html', {'pathfinder_response': pathfinder_response, 'pathfinder_api_url': reverse('chatbot')})

def index(request):
    return render(request, 'index.html')


def gdpr(request):
    return render(request, 'gdpr.html')


def about(request):
    return render(request, 'about.html')

def notemaker(request):
    return render(request, 'notemaker.html')

def games(request):
    return render(request, 'games.html')

def brickbreaker(request):
    return render(request, 'brickbreaker.html')


# def chatwindow(request):
    # return render(request, 'chatwindow.html')


def chatbot(chat_query_response):
    openai.api_key = api_key
    gpt_response = ''
    prompt = "Welcome the user and ask them what they want to learn about."

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


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(
                request, ("There was an error logging in, try again..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out."))
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Account successfuly created!"))
            return redirect('index')
    else:
        form = RegisterUserForm()

    return render(request, 'signup.html', {'form': form, })


# googlesign in


def logout_view(request):
    logout(request)
    return redirect("index")


def signup_redirect(request):
    messages.error(
        request, "Something wrong here, it may be that you already have account!")
    return redirect("index")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    # Handle user login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.username)
            request.session['username'] = user.username
            return redirect('home')
        else:
            # Handle login failure
            pass
    else:
        # Display login page
        return render(request, 'login.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UpdateProfile(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/profile')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = UpdateProfile(instance=request.user)

    return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})

def profile(request):
    context = {}
    return render(request, 'profile.html', context)