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
]



urlpatterns += staticfiles_urlpatterns()