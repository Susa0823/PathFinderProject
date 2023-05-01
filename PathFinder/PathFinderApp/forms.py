from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserChatPrompt, User
from django.forms import ModelForm, fields
from . models import Notes


class ChatBotForm(forms.ModelForm):
    class Meta:
        model = UserChatPrompt
        fields = ['user_query']

    def t(self):
        data = self.cleaned_data
        prompt = data['user_query']
        response = data['pathfinder_response']
        return prompt, response

#     user_query, pathfinder_response = None, None
    user_query = forms.CharField(label='User Query', max_length=1000)
    pathfinder_response = forms.CharField(
       label='PathFinder Response', max_length=1000)


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email'}))
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        # self.fields['username'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-sm', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control form-control-sm', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-sm', 'placeholder': 'Confirm Password'})
        # self.fields['password1'].widget.attrs['class'] = 'form-control form-control-sm'
        # self.fields['password2'].widget.attrs['class'] = 'form-control form-control-sm'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        
       


    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            return self.instance.username
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            return self.instance.first_name
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            return self.instance.last_name
        return last_name
    
class UpdateProfile(forms.ModelForm):
    profile_picture =  forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}),required=True)

    class Meta:
        model = User
        fields = ('profile_picture',)




# NotesPage
class NotesForm(ModelForm):
    heading = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder":"Enter Title"
    }))
    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
         "class": "form-control", "placeholder":"Enter Notes", "rows":"8"
    }))
    class Meta:
        model = Notes
        fields = ['heading', 'text']

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Your Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Name'}))
    
    email = forms.EmailField(
        label='Your Email',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'}))
    
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': 5, 'placeholder': 'Message'}))
    
    def send_email(self):
        # logic to send email
        pass