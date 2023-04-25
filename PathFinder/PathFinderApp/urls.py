from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('', views.index, name='index'),
    # path('chatbot', views.chatbot, name='chatbot')
    # path('about', views.about, name='about'),
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('policy/', views.gdpr, name='policy'),
    path('about/', views.about, name='about'),
    path('notemaker/', views.notemaker, name='notemaker'),
    path('chatbox/', views.test_chatbotview, name='chatbox'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('signin/', views.register_user, name="register_user"),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]


urlpatterns += staticfiles_urlpatterns()
