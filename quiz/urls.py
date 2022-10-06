from django.urls import path
from . import views

from quiz.views import QuizView, QuizzesView, LeaderBoard, QuizLeaderBoard, QuestionView, CheckResponses, \
    CheckQuizPlayedOrNot

urlpatterns = [
    path("", QuizzesView.as_view()),
    path("leaderboard/results/", LeaderBoard.as_view()),
    path("leaderboard/results/<str:pk>/", QuizLeaderBoard.as_view()),
    path("questions/", views.question),

    path("question/<int:pk>/", QuestionView.as_view()),
    path("checkresponses/", CheckResponses.as_view()),
    path("checkPlayedOrNot/", CheckQuizPlayedOrNot.as_view()),
    path("<uuid:pk>/", QuizView.as_view()),
]