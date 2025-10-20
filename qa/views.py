from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Вопрос номер {i}',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi.',
        'rating': random.randint(-10, 100),
        'answers_count': random.randint(0, 20),
        'tags': ['python', 'django', 'bootstrap']
    } for i in range(30)
]

def index(request):
    context = {'questions': QUESTIONS}
    return render(request, 'index.html', context)

def hot_questions(request):
    best_questions = sorted(QUESTIONS, key=lambda q: q['rating'], reverse=True)
    context = {'questions': best_questions}
    return render(request, 'index.html', context)    

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
            'text': f'Ответ на вопрос №{i}. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'rating': random.randint(-10, 50),
        } for i in range(5)
    ]

    context = {
        'question': q,
        'answers': answer,
    }

    return render(request, 'question.html', context)

def question_by_tag(request, tag_name):
    tagged_questions = []
    for q in QUESTIONS:
        if tag_name in q['tags']:
            tagged_questions.append(q)

    context = {
        'questions': tagged_questions,
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)
