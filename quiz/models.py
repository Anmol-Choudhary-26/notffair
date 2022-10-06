from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import DurationField
# from django.forms import CharField, DateTimeField, IntegerField, URLField
from user.models import Users

class Quiz(models.Model):
    id = models.CharField(primary_key=True,default=uuid4(),max_length=250)
    name = models.CharField('name',max_length=250,null=False)
    clubname = models.CharField('clubname',max_length=250,null=False)
    count = models.IntegerField('count',default=0)
    sendCount = models.IntegerField('sendCount',default=True)
    startTime = models.DateTimeField('startTime',null=False,help_text='Format: YYYY-MM-DDThh:mm, example 2021-01-01T15:30')
    endTime = models.DateTimeField('endTime',null=False,help_text='Format: YYYY-MM-DDThh:mm, example 2021-01-01T15:30')
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return "Quiz" + self.name



class Answer(models.Model):
    text = models.CharField('text',max_length=250,blank=True,null=True)
    image = models.URLField('image',blank=True,null=True)


class Question(models.Model):
    text = models.CharField('text',max_length=500)
    image = models.URLField('image',blank=True,null=True)
    optionCount = models.IntegerField("optionCount", default=4,
                    validators= [MaxValueValidator(4), MinValueValidator(2)])

    option1 = models.ForeignKey(Answer,related_name='option1', on_delete=models.CASCADE)
    option2 = models.ForeignKey(Answer,related_name='option2', on_delete=models.CASCADE)
    option3 = models.ForeignKey(Answer,related_name='option3', on_delete=models.CASCADE)
    option4 = models.ForeignKey(Answer,related_name='option4', on_delete=models.CASCADE)

    correct = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    timeLimit = models.IntegerField("timeLimit",default=15)

    marks = models.PositiveIntegerField("marks",default=5)
    negativeMarks = models.PositiveIntegerField("negativeMarks",default=0) # negative marks per question


# if two have same score the calculate the average time
class ScoreBoard(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField("timestamp")

    class Meta:
        ordering = ['-score','-timestamp']

    def _str__(self):
        return self.user.email


class QuizScoreBoard(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField("timestamp")

    class Meta:
        unique_together = ("user","quiz")

    def __str__(self):
        return self.user.email + " " + self.quiz.name
