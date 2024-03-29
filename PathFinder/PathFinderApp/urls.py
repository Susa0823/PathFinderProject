from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import ChangePasswordView


urlpatterns = [
    # path('', views.index, name='index'),
    # path('chatbot', views.chatbot, name='chatbot')
    # path('about', views.about, name='about'),
    path("", views.index, name="index"),
    # path('chatbot/', views.chatbot, name='chatbot'),
    path("policy/", views.gdpr, name="policy"),
    path("about/", views.about, name="about"),
    path("chatbox/response", views.send_chat_response, name="chatbot"),
    path("chatbox/", views.render_chatbotview, name="chatbox"),
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name="logout"),
    # path('signup/', views.register_user, name="register_user"),
    # path('social/signup/', views.signup_redirect, name='signup_redirect'),
    # path('profile/', views.profile, name='profile'),
    path("edit/", views.edit_profile, name="edit"),
    path("bloghome/", views.bloghome, name="bloghome"),
    path("profilelist/", views.profilelist, name="profilelist"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("update_user/", views.update_user, name="update_user"),
    path("meep_like/<int:pk>", views.meep_like, name="meep_like"),
    path("meep_show/<int:pk>", views.meep_show, name="meep_show"),
    # For Games
    path("games/", views.games, name="games"),
    path("brickbreaker/", views.brickbreaker, name="brickbreaker"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.edit_profile, name="edit"),
    path("remembergame/", views.remembergame, name="remembergame"),
    path("rockps/", views.rockps, name="rockps"),
    path("tictakpro/", views.tictakpro, name="tictakpro"),
    # For Notmaker
    path("notemaker/", views.noteindex, name="noteindex"),
    path("new_note", views.new_note, name="new"),
    path("note/<str:pk>", views.note_detail, name="note"),
    path("delete_note/<str:pk>", views.delete_note, name="delete"),
    path("search_result", views.search_page, name="search"),
    path("password/", ChangePasswordView.as_view(), name="password"),
]


urlpatterns += staticfiles_urlpatterns()
