from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Answer, Tag
from .utils import paginate
from django.db.models import Count

# Create your views here.

def index(request):
    questions = Question.objects.all().order_by('-created_at')
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
    questions = tag.question_set.all().order_by('-created_at')
    page_obj = paginate(questions, request, per_page=10)

    context = {
        'questions': page_obj,
        'tag_name': tag_name,
    }

    return render(request, 'qa/tag.html', context)

def login_view(request):
    return render(request, 'qa/login.html')

def signup_view(request):
    return render(request, 'qa/signup.html')

def ask_question(request):
    return render(request, 'qa/ask.html')
