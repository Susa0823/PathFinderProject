from django import forms

class ChatBotForm(forms.Form):
    user_query = forms.CharField(label='User Query', max_length=1000)
    pathfinder_response = forms.CharField(label='PathFinder Response', max_length=1000)
