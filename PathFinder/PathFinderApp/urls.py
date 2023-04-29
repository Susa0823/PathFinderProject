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
    path('chatbox/', views.test_chatbotview, name='chatbox'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.register_user, name="register_user"),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
    path('profile/', views.profile, name='profile'),
    path('edit/',views.edit_profile, name = 'edit'),


    # For Games
    path('games/', views.games, name='games'),
    path('brickbreaker/', views.brickbreaker, name='brickbreaker'),
    path('remembergame/', views.remembergame, name='remembergame'),
    path('rockps/', views.rockps, name='rockps'),
    path('tictakpro/', views.tictakpro, name='tictakpro'),
    

    # For Notmaker
    path('notemaker/', views.noteindex, name = 'noteindex'),
    path('new_note', views.new_note, name = 'new'),
    path('note/<str:pk>', views.note_detail, name = 'note'),
    path('delete_note/<str:pk>', views.delete_note, name = 'delete'),
    path('search_result', views.search_page, name = 'search'),

]


urlpatterns += staticfiles_urlpatterns()
