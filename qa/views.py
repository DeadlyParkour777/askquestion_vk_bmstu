from django.shortcuts import render
from django.http import HttpResponse
from .utils import paginate
import random

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Вопрос номер {i + 1}',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi.',
        'rating': random.randint(-10, 100),
        'answers_count': random.randint(0, 20),
        'tags': ['python', 'django', 'bootstrap']
    } for i in range(30)
]

def index(request):
    page_obj = paginate(QUESTIONS, request, per_page=5)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)

def hot_questions(request):
    best_questions = sorted(QUESTIONS, key=lambda q: q['rating'], reverse=True)
    page_obj = paginate(best_questions, request, per_page=5)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)    

def question_info(request, question_id):
    q = None
    for question in QUESTIONS:
        if question['id'] == question_id:
            q = question
            break
    
    if q == None:
        return HttpResponse('Question not found')

    answer = [
        {
            'text': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'rating': random.randint(-10, 50),
        } for _ in range(q['answers_count'])
    ]

    context = {
        'question': q,
        'answers': answer,
    }

    return render(request, 'qa/question.html', context)

def question_by_tag(request, tag_name):
    tagged_questions = []
    for q in QUESTIONS:
        if tag_name in q['tags']:
            tagged_questions.append(q)

    context = {
        'questions': tagged_questions,
        'tag_name': tag_name,
    }

    return render(request, 'qa/tag.html', context)

def login_view(request):
    return render(request, 'qa/login.html')

def signup_view(request):
    return render(request, 'qa/signup.html')

def ask_question(request):
    return render(request, 'qa/ask.html')
