from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Question, Answer, Tag
from .utils import paginate
from .forms import SignupForm, LoginForm, AskForm
from django.db.models import Count

# Create your views here.

def index(request):
    questions = Question.objects.all().annotate(answers_count=Count('answer')).order_by('-created_at')
    page_obj = paginate(questions, request, per_page=10)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)

def hot_questions(request):
    questions = Question.objects.annotate(num_answers=Count('answer')).order_by('-num_answers')
    page_obj = paginate(questions, request, per_page=10)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)    

def question_info(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.order_by('-created_at')

    context = {
        'question': question,
        'answers': answers,
    }

    return render(request, 'qa/question.html', context)

def question_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.question_set.all().annotate(answers_count=Count('answer')).order_by('-created_at')
    page_obj = paginate(questions, request, per_page=10)

    context = {
        'questions': page_obj,
        'tag_name': tag_name,
    }

    return render(request, 'qa/tag.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'qa/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'qa/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def ask_view(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(author=request.user.profile)
            return redirect('question', question_id=question.id)
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})
