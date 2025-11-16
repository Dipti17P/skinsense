from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_quiz, name='quiz_start'),
    path('question/<int:qid>/', views.quiz_question, name='quiz_question'),
    path('result/', views.quiz_result, name='quiz_result'),
    path('progress/', views.track_progress, name='track_progress'),
    
]
