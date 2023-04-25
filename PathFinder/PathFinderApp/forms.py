from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class ChatBotForm(forms.Form):
    user_query = forms.CharField(label='User Query', max_length=1000)
    pathfinder_response = forms.CharField(
        label='PathFinder Response', max_length=1000)


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email'}))
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Name'}))
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
