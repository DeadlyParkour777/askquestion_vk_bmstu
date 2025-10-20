from django.shortcuts import render
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
