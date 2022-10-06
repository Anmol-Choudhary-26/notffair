from asyncio import events
from http.client import ImproperConnectionState
from multiprocessing import Event
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from adminUser.models import AdminUser
from events.models import Events
from coupons.models import Coupon
from store.models import ProductImage
from store.models import Store
from .forms import CreateQuestionForm, QuizForm, LoginForm, QuizFormCoupon, QuizFormEvent, QuizFormStore
from quiz.models import Quiz, Question, QuizScoreBoard, ScoreBoard, Answer
from django.contrib.auth.mixins import LoginRequiredMixin
from uuid import uuid1
import xlwt
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth import login, logout

# Create your views here.

class LoginView(View):

    def get(self, request):
        return render(request, template_name="auth/login.html", context={"form": LoginForm(), "title": "Login"})

    def post(self, request):
        data = request.POST
        try:
            adminUser = AdminUser.objects.get(name=data['name'])
        except AdminUser.DoesNotExist:
            return render(request, template_name="auth/login.html",
                          context={"form": LoginForm(), "title": "Login", "message": "Invalid adminUser Name."})

        if adminUser.user.check_password(data['password']):
            login(request, adminUser.user)
            return HttpResponseRedirect(reverse_lazy("quizPanelHome"))
        else:
            return render(request, template_name="auth/login.html",
                          context={"form": LoginForm(), "title": "Login", "message": "Invalid Password"})


class LogoutView(View):

    def get(self, request):
        return render(request, template_name="auth/logout.html", context={"title": "Logout"})

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('quizPanelLogin'))


class CreateQuestionView(LoginRequiredMixin, View):

    def get(self, request, id):
        return render(request, template_name="quiz/create-question.html",
                      context={"form": CreateQuestionForm(), "title": "Create Question"})

    def post(self, request, id):
        quiz = get_object_or_404(Quiz, pk=id)
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            option1 = Answer.objects.create(
                text=data['option_1'],
                image=data['image_1']
            )
            option2 = Answer.objects.create(
                text=data['option_2'],
                image=data['image_2']
            )
            option3 = Answer.objects.create(
                text=data['option_3'],
                image=data['image_3']
            )
            option4 = Answer.objects.create(
                text=data['option_4'],
                image=data['image_4']
            )
            option1.save()
            option2.save()
            option3.save()
            option4.save()
            question = Question.objects.create(
                text=data["question_statement"],
                image = data["image"],
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                quiz_id=id,
                correct=getCorrectOption(option1, option2, option3, option4, int(data['correct_option'])),
                timeLimit=data['timeLimit'],
                optionCount=data['optionCount'],
                marks=data['marks'],
                negativeMarks=data['negativeMarks'],
            )
            question.save()
            quiz.count = quiz.count + 1
            quiz.save()

            return HttpResponseRedirect(reverse_lazy("quizPanelQuizDetails", kwargs={"id": id}))
        else:
            return render(request, template_name="quiz/create-question.html",
                          context={"form": CreateQuestionForm(), "title": "Create Question"})


class UpdateQuestionView(LoginRequiredMixin, View):

    def get(self, request, id):
        question = Question.objects.get(id=id)
        form = CreateQuestionForm(
            initial={
                "correct_option": getCorrectNumber(question.option1, question.option2, question.option3,
                                                   question.correct),
                "image": question.image,
                "optionCount": question.optionCount,
                "option_1": question.option1.text,
                "image_1": question.option1.image,
                "option_2": question.option2.text,
                "image_2": question.option2.image,
                "option_3": question.option3.text,
                "image_3": question.option3.image,
                "option_4": question.option4.text,
                "image_4": question.option4.image,
                "question_statement": question.text,
                "timeLimit": question.timeLimit,
                'marks': question.marks,
                'negativeMarks': question.negativeMarks
            }
        )
        return render(request, template_name="quiz/update-question.html",
                      context={"form": form, "title": "Update Question"})

    def post(self, request, id):
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            question = Question.objects.get(id=id)
            option1 = Answer.objects.get(id=question.option1.id)
            option2 = Answer.objects.get(id=question.option2.id)
            option3 = Answer.objects.get(id=question.option3.id)
            option4 = Answer.objects.get(id=question.option4.id)
            
            option1.text = data["option_1"]
            option1.image = data["image_1"]

            option2.text = data["option_2"]
            option2.image = data["image_2"]

            option3.text = data["option_3"]
            option3.image = data["image_3"]

            option4.text = data["option_4"]
            option4.image = data["image_4"]


            option1.save()
            option2.save()
            option3.save()
            option4.save()
            question.correct = getCorrectOption(option1, option2, option3, option4, int(data["correct_option"]))
            question.timeLimit = data["timeLimit"]
            question.optionCount = data["optionCount"]
            question.image = data["image"]
            question.text = data["question_statement"]
            question.marks = data["marks"]
            question.negativeMarks = data["negativeMarks"]
            question.save()
            return HttpResponseRedirect(reverse_lazy("quizPanelQuizDetails", kwargs={"id": question.quiz.id}))
        else:
            return render(request, template_name="quiz/update-question.html",
                          context={"form": form, "title": "Update Question"})

class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        quizzes = Quiz.objects.all()
        events = Events.objects.all()
        stores = Store.objects.all()
        coupons = Coupon.objects.all()
        return render(request, template_name="quiz/Home.html", context={"title": "Home", "quizzes": quizzes,"events":events,"stores":stores,"coupons":coupons})


class QuizView(LoginRequiredMixin, View):

    def get(self, request, id):
        quiz = get_object_or_404(Quiz, pk=id)
        questions = Question.objects.all().filter(quiz_id=quiz.id)
        return render(request, template_name="quiz/quiz-details.html",
                      context={"title": "Quiz Details", "quiz": quiz, "questions": questions})


class CreateQuizView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name="quiz/create-quiz.html",
                      context={"form": QuizForm(), "title": "Create Quiz"})

    def post(self, request):
        form = QuizForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quiz = Quiz.objects.create(
                id=uuid1(),
                name=data["name"],
                startTime=data["startTime"],
                endTime=data["endTime"],
                sendCount=data["sendCount"],
                clubname = data["clubname"],
            )
            quiz.save()
            return HttpResponseRedirect(reverse_lazy('quizPanelHome'))
        else:
            return render(request, template_name="quiz/create-quiz.html",
                          context={"form": form, "title": "Create Quiz"})


class UpdateQuizView(LoginRequiredMixin, View):
    def get(self, request, id):
        quiz = Quiz.objects.get(id=id)
        form = QuizForm(instance=quiz)
        return render(request, template_name="quiz/update-quiz.html",
                      context={"form": form, "title": "Update Quiz"})

    def post(self, request, id):
        form = QuizForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quiz = get_object_or_404(Quiz, pk=id)
            quiz.startTime = data['startTime']
            quiz.endTime = data['endTime']
            quiz.name = data['name']
            quiz.count = 0
            quiz.sendCount = data['sendCount']
            quiz.clubname = data['clubname']
            quiz.save()
            return HttpResponseRedirect(reverse_lazy('quizPanelQuizDetails', kwargs={"id": id}))
        else:
            return render(request, template_name="quiz/update-quiz.html",
                          context={"form": form, "title": "Update Quiz"})


class UploadQuestionUsingExcelSheetView(LoginRequiredMixin, View):
    def get(self, request, id):
        quiz = get_object_or_404(Quiz, pk=id)
        return render(request, "quiz/excelUpload.html", {"title": "Question Upload", "quiz": quiz})

    def post(self, request, id):
        quiz = get_object_or_404(Quiz, pk=id)
        file = request.FILES['file']
        data = pd.read_excel(file)
        questions = data.to_dict('records')
        for question in questions:
            for key in question:
                if str(question[key])=='nan':
                    question[key] = ''
                    if key=='optionCount':
                        question[key] = 4
            try:
                option1 = Answer(
                    text=str(question['Option 1']),
                    image=str(question['Image 1'])
                )
                option2 = Answer(
                    text=str(question['Option 2']),
                    image=str(question['Image 2'])
                )
                option3 = Answer(
                    text=str(question['Option 3']),
                    image=str(question['Image 3'])
                )
                option4 = Answer(
                    text=str(question['Option 4']),
                    image=str(question['Image 4'])
                )
                option1.save()
                option2.save()
                option3.save()
                option4.save()

                q = Question.objects.create(
                    quiz_id=id,
                    text=str(question['Question Text']),
                    image=str(question['Image']),
                    optionCount=int(question['Option Count']),
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct=getCorrectOption(option1, option2, option3, option4,
                                                int(question['Correct Option(1-4)'])),
                    timeLimit = question['Time Limit'],
                    marks = question['Marks'],
                    negativeMarks = question['Negative Marks']
                )
                q.save()
                quiz.count = quiz.count + 1
                quiz.save()
            except Exception as e:
                pass

        return HttpResponseRedirect(reverse_lazy('quizPanelQuizDetails', kwargs={'id': quiz.id}))


class LeaderBoardView(LoginRequiredMixin, View):
    def get(self, request, id):
        quiz = get_object_or_404(Quiz, pk=id)
        ranking = QuizScoreBoard.objects.all().filter(quiz=quiz).order_by('-score')
        return render(request, "quiz/leaderboard.html", {"quiz": quiz, "results": ranking, "title": "LeaderBoard"})


class ChooseQuizView(LoginRequiredMixin, View):
    def get(self, request):
        quizzes = Quiz.objects.all()
        return render(request, template_name="quiz/select-quiz.html",
                      context={"title": "Choose Quiz", "quizzes": quizzes})


def export_leaderboard_xls(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    ranking = QuizScoreBoard.objects.all().filter(quiz=quiz).order_by('-score')
    response = HttpResponse(content_type='application/ms-excel')
    filename = quiz.name.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('LeaderBoard')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Ranking', 'First name', 'Last name', 'Email address', 'Phone', 'Score']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    for row in ranking:
        row_num += 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, row.user.firstName, font_style)
        ws.write(row_num, 2, row.user.lastName, font_style)
        ws.write(row_num, 3, row.user.email, font_style)
        ws.write(row_num, 4, row.user.phone, font_style)
        ws.write(row_num, 5, row.score, font_style)

    font_style = xlwt.XFStyle()
    wb.save(response)
    return response


class DeleteQuizQuestionView(LoginRequiredMixin, View):
    def get(self, request, id):
        question = get_object_or_404(Question, pk=id)
        return render(request, "quiz/delete_question.html", {"title": "Delete Question", "question": question})

    def post(self, request, id):
        question = get_object_or_404(Question, pk=id)
        quizId = question.quiz.id
        quiz = get_object_or_404(Quiz, pk=quizId)
        quiz.count = quiz.count - 1
        quiz.save()
        question.delete()
        return HttpResponseRedirect(reverse_lazy("quizPanelQuizDetails", kwargs={"id": quizId}))


def getCorrectOption(option1, option2, option3, option4, correct):
    if correct == 1:
        return option1
    elif correct == 2:
        return option2
    elif correct == 3:
        return option3
    else:
        return option4


def getCorrectNumber(option1, option2, option3, correctOption):
    if correctOption == option1:
        return 1
    elif correctOption == option2:
        return 2
    elif correctOption == option3:
        return 3
    else:
        return 4




# Events Section
class CreateEventView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name="quiz/create-event.html",
                      context={"form": QuizFormEvent(), "title": "Create Event"})

    def post(self, request):
        form = QuizFormEvent(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            event = Events.objects.create(
                title=data["title"],
                description=data["description"],
                startTime=data["startTime"],
                endTime=data["endTime"],
                clubName = data["clubName"],
                platform = data["platform"],
                image = data["image"],
                regURL = data["regURL"],
                type = data['typesel']
            )
            event.save()
            return HttpResponseRedirect(reverse_lazy('quizPanelHome'))
        else:
            return render(request, template_name="quiz/create-event.html",
                          context={"form": form, "title": "Create Event"})
        
class EventView(LoginRequiredMixin, View):
    
    def get(self, request, title):
        event = get_object_or_404(Events, title=title)
        return render(request, template_name="quiz/event-details.html",
                      context={"title": "Event Details", "event": event,})


# Store Section
class CreateStoreView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name="quiz/create-store.html",
                      context={"form": QuizFormStore(), "title": "Create Store"})

    def post(self, request):
        form = QuizFormStore(request.POST)
        if form.is_valid():
            uid = uuid1()
            data = form.cleaned_data
            store = Store.objects.create(
                id=uid,
                productName=data["productName"],
                price=data["price"],
                description=data["description"],
                clubName = data["clubName"],
                payment = data["payment"],
            )
            store.save()
            store1 = Store.objects.get(id=uid)
            productimage = ProductImage.objects.create(
                product = store1,
                imageUrl1 = data['imageUrl1'],
                imageUrl2 = data['imageUrl2']
            )
            # print(productimage.product)
            # print(productimage.imageUrl1)
            productimage.save()
            return HttpResponseRedirect(reverse_lazy('quizPanelHome'))
        else:
            return render(request, template_name="quiz/create-store.html",
                          context={"form": form, "title": "Create Store"})

class StoreView(LoginRequiredMixin, View):
    
    def get(self, request, id):
        store = get_object_or_404(Store, pk=id)
        product = get_object_or_404(ProductImage,product=store)
        # questions = Question.objects.all().filter(quiz_id=quiz.id)
        return render(request, template_name="quiz/store-details.html",
                      context={"title": "Store Details", "store": store,"product":product})


# Coupon Section
class CreateCouponView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name="quiz/create-coupon.html",
                      context={"form": QuizFormCoupon(), "title": "Create Coupon"})

    def post(self, request):
        form = QuizFormCoupon(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            coupon = Coupon.objects.create(
                coupon_name=data["coupon_name"],
                # created=data["created"],
                # updated=data["updated"],
                code=data["code"],
                code_l = data["code_l"],
                value = data["value"],
                repeat = data["repeat"],
            )
            coupon.save()
            return HttpResponseRedirect(reverse_lazy('quizPanelHome'))
        else:
            return render(request, template_name="quiz/create-coupon.html",
                          context={"form": form, "title": "Create Coupon"})
        
