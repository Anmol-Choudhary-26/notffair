from django.contrib import admin

from quiz.models import ScoreBoard, Quiz, QuizScoreBoard, Question, Answer

admin.site.register(QuizScoreBoard)
admin.site.register(Quiz)
admin.site.register(ScoreBoard)
admin.site.register(Question)
admin.site.register(Answer)