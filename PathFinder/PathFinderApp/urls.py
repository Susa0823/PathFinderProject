from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('chatbot', views.chatbot, name='chatbot')
    # path('about', views.about, name='about'),
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
]
