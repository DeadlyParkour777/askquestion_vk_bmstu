from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'), 
    path('hot/', views.hot_questions, name='hot'),
    path('question/<int:question_id>/', views.question_info, name='question'),
    path('tag/<str:tag_name>/', views.question_by_tag, name='tag'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('ask/', views.ask_view, name='ask'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('vote/question/', views.vote_question, name='vote_question'),
    path('vote/answer/', views.vote_answer, name='vote_answer'),
    path('correct/', views.mark_correct, name='mark_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
