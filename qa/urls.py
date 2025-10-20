from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('hot/', views.hot_questions, name='hot'),
    path('question/<int:question_id>/', views.question_info, name='question')
]
