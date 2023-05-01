from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
import json
# import pickle
import warnings
import openai
import pinecone
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
from .models import Notes
from .forms import NotesForm
from django.contrib.auth.models import User
import smtplib
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage



api_key = os.environ.get('OPENAI_API_KEY')

# warnings.filterwarnings("ignore")


def qachain(request):

    # qamodel.load_embed_pickle()
    pinecone.init(api_key='5bf2927b-0fb7-423b-b8f1-2f6a3347a15d',
                  environment='asia-northeast1-gcp')
    vectorstore = Pinecone.from_existing_index(
        'teamprojindex', OpenAIEmbeddings())
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
    vectorstore = Pinecone.from_existing_index(
        'teamprojindex', OpenAIEmbeddings())

    message = "The user is about to enter a conversation with you, greet them and let them know what you can do."

    ChatBotForm()
    pathfinder_chatbot = qamodel.make_chain(vectorstore)

    if request.method == 'POST':
        message = request.POST.get('chat-input')
        # print(message)
        # print('message is not none')

    #! form = ChatBotForm(request.POST or None)
    if message=='':
        # TODO: Obviously a temporary fix
        message= 'I\'ve sent you an empty message, I will try again.'
    if message is not None:
        response = pathfinder_chatbot({
            "question": message,
            # "name": name,
            "chat_history": []
        })  # query the chatbot

    # # form = ChatBotForm(request.POST or None)
    # # content = {
    # #     'form': form
    # # }
    # # if form.is_valid():
    # #     chat_prompt = form.save()
    # #     print(chat_prompt)
    # #     content['form'] = ChatBotForm()
    # #     name = form.cleaned_data['name']
    # message = form.cleaned_data['message']
    # #     return JsonResponse({'response': response})
    # else:
    #     form = ChatBotForm(request.POST)
    # test ={
    #     'name': request.user.username,
    # }
    # return render(request, 'chatwindow.html', context=content)
    pathfinder_response = response['answer']

    return render(request, 'chatwindow.html', {'pathfinder_response': pathfinder_response, 'user_message': message})


def index(request):
    return render(request, 'index.html')


def gdpr(request):
    return render(request, 'gdpr.html')


def about(request):
    return render(request, 'about.html')

# For the Games Page
def games(request):
    return render(request, 'games.html')

def brickbreaker(request):
    return render(request, 'brickbreaker.html')

def remembergame(request):
    return render(request, 'remem.html')

def rockps(request):
    return render(request, 'rockps.html')

def tictakpro(request):
    return render(request, 'tictakpro.html')

# For the Notemaker Page
def noteindex(request):
    notes = Notes.objects.all()
    return render(request, "noteindex.html", {"notes": notes})

def new_note(request):
    form = NotesForm()
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("noteindex")
    return render(request, "noteupdate.html", {"form": form})

def note_detail(request, pk):
    note = Notes.objects.get(id=pk)
    form = NotesForm(instance=note)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("noteindex")
    return render(request, "noteupdate.html", {"note": note, "form": form})

# def delete_note(request, pk):
def delete_note(request, pk):
    note = Notes.objects.get(id=pk)
    form = NotesForm(instance=note)
    if request.method == 'POST':
        note.delete()
        messages.info(request, "The note has been deleted")
    return render(request, "notedelete.html", {"note": note, "form": form})

def search_page(request):
    if request.method == 'POST':
        search_text = request.POST['search']
        notes = Notes.objects.filter(heading__icontains = search_text) | Notes.objects.filter(text__icontains = search_text)
        # if notes is None:
        #     messages.info(request, "Note not found")
        return render(request, "notesearch.html", {"notes": notes})
    



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

def edit_profile(request):
    
    if not request.user.is_authenticated:
        return redirect('/login')
    
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

    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})

def profile(request):
    context = {}
    return render(request, 'profile.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            email_subject = 'New Contact Form Submission'
            email_body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
            email = EmailMessage(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                reply_to=[email],
            )
            email.from_email = email
            email.send(fail_silently=False)

            return render(request, 'thanks.html')
    else:
        form = ContactForm()
    return render(request, 'form.html', {'form': form})