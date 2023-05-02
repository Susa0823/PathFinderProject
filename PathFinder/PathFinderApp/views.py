from django.contrib.auth import authenticate, login
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
from .forms import EditProfileForm, UpdateProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Notes
from .forms import NotesForm, ContactForm
from django.contrib.auth.models import User
import smtplib
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import os
import json
# import pickle
# import warnings
import openai
import pinecone
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView


api_key = os.environ.get('OPENAI_API_KEY')

# warnings.filterwarnings("ignore")

pinecone.init(api_key='5bf2927b-0fb7-423b-b8f1-2f6a3347a15d',
              environment='asia-northeast1-gcp')
vectorstore = Pinecone.from_existing_index(
    'teamprojindex', OpenAIEmbeddings())
pathfinder_chatbot = qamodel.make_chain(vectorstore)


def render_chatbotview(request):
    # # print(request.POST)
    # print('ran')
    return render(request, 'chatwindow.html')


def send_chat_response(request):
    pathfinder_response = ""

    if request.method == 'POST':
        json_user_input = json.loads(request.body)
        user_message = json_user_input['user_message']
        if user_message is not None:
            response = pathfinder_chatbot({
                "question": user_message,
                # [("Q","A")]
                "chat_history": [("", "")],
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

### For the Games Page ###


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

### For the Notemaker Page ###


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
        notes = Notes.objects.filter(heading__icontains=search_text) | Notes.objects.filter(
            text__icontains=search_text)
        # if notes is None:
        #     messages.info(request, "Note not found")
        return render(request, "notesearch.html", {"notes": notes})

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


# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.success(
#                 request, ("There was an error logging in, try again..."))
#             return redirect('login')
#     else:
#         return render(request, 'login.html', {})


# def logout_user(request):
#     logout(request)
#     messages.success(request, ("You have successfully logged out."))
#     return redirect('index')


# def register_user(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, ("Account successfuly created!"))
#             return redirect('index')
#     else:
#         form = RegisterUserForm()

#     return render(request, 'signup.html', {'form': form, })


### Google sign in ###


# def logout_view(request):
#     logout(request)
#     return redirect("index")


# def signup_redirect(request):
#     messages.error(
#         request, "Something wrong here, it may be that you already have account!")
#     return redirect("index")

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def login_view(request):
#     # Handle user login
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print(user.username)
#             request.session['username'] = user.username
#             return redirect('home')
#         else:
#             # Handle login failure
#             pass
#     else:
#         # Display login page
#         return render(request, 'bloglogin.html')

def edit_profile(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UpdateProfile(
            request.POST, request.FILES, instance=request.user)

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

# def profile(request):
#     context = {}
#     return render(request, 'profile.html', context)


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


#For Blog
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


def bloghome(request):
	if request.user.is_authenticated:
		form = MeepForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				meep = form.save(commit=False)
				meep.user = request.user
				meep.save()
				messages.success(request, ("Your Discovery Has Been Posted!"))
				return redirect('bloghome')
		
		meeps = Meep.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"meeps":meeps, "form":form})
	else:
		meeps = Meep.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"meeps":meeps})



def profilelist(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('bloghome')

def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")

		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "meeps":meeps})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('bloghome')	
                        
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('bloghome')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})

# def logout_user(request):
#     return render(request, 'profile_list.html')

def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out. Till we meet again..."))
	return redirect('index')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('bloghome')
	
	return render(request, "signup.html", {'form':form})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = EditProfileForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			#login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('bloghome')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('bloghome')
	
def meep_like(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		if meep.likes.filter(id=request.user.id):
			meep.likes.remove(request.user)
		else:
			meep.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))




	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('bloghome')


def meep_show(request, pk):
	meep = get_object_or_404(Meep, id=pk)
	if meep:
		return render(request, "show_meep.html", {'meep':meep})
	else:
		messages.success(request, ("That Post Does Not Exist..."))
		return redirect('bloghome')		


def my_view(request):
    # Get the current user
    user = request.user

    # Get the user's first name
    first_name = user.first_name

    # Add the first name to the context dictionary
    context = {
        'first_name': first_name
    }

    return render(request, 'my_template.html', context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'password.html'
    success_message = "Successfully changed your pasword"
    success_url = reverse_lazy('profile')
