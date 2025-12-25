from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Question, Answer, Tag, AnswerVote, QuestionVote
from .utils import paginate
from .forms import SignupForm, LoginForm, AskForm, SettingsForm, AnswerForm
from django.db.models import Count

# Create your views here.

def index(request):
    questions = Question.objects.all().annotate(answers_count=Count('answer')).order_by('-created_at')
    page_obj = paginate(questions, request, per_page=10)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)

def hot_questions(request):
    questions = Question.objects.annotate(answers_count=Count('answer')).order_by('-rating', 'created_at')
    page_obj = paginate(questions, request, per_page=10)
    context = {'questions': page_obj}
    return render(request, 'qa/index.html', context)    

def question_info(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.order_by('-created_at')
    form = AnswerForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(request.user, question)
            return redirect(f'/question/{question.id}/#answer-{answer.id}')

    context = {
        'question': question,
        'answers': answers,
        'form': form,
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
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
                next_url = request.GET.get('continue', request.GET.get('next', 'index'))
                return redirect(next_url)
            form.add_error(None, 'Неверный логин или пароль')
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
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', 'index'))
    return redirect(next_url)

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

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = SettingsForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
        }
        form = SettingsForm(request.user, initial=initial_data)

    return render(request, 'qa/settings.html', {'form': form})

@require_POST
@login_required
def vote_question(request):
    question_id = request.POST.get('question_id')
    value = request.POST.get('value')
    
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    
    if user.profile == question.author:
        return JsonResponse({'error': 'Нельзя голосовать за свой вопрос'}, status=403)

    vote, created = QuestionVote.objects.get_or_create(user=user, question=question)
    
    if value == 'like':
        vote.value = 1
    elif value == 'dislike':
        vote.value = -1
    else:
        return JsonResponse({'error': 'Неверное действие'}, status=400)
    
    vote.save()
    
    rating = sum(v.value for v in QuestionVote.objects.filter(question=question))
    question.rating = rating
    question.save()
    
    return JsonResponse({'rating': rating})

@require_POST
@login_required
def vote_answer(request):
    answer_id = request.POST.get('answer_id')
    value = request.POST.get('value')
    
    answer = get_object_or_404(Answer, pk=answer_id)
    user = request.user

    if user.profile == answer.author:
        return JsonResponse({'error': 'Нельзя голосовать за свой ответ'}, status=403)

    vote, created = AnswerVote.objects.get_or_create(user=user, answer=answer)
    
    if value == 'like':
        vote.value = 1
    elif value == 'dislike':
        vote.value = -1
    else:
        return JsonResponse({'error': 'Неверное действие'}, status=400)
    
    vote.save()
    
    rating = sum(v.value for v in AnswerVote.objects.filter(answer=answer))
    answer.rating = rating
    answer.save()
    
    return JsonResponse({'rating': rating})

@require_POST
@login_required
def mark_correct(request):
    answer_id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question

    if request.user.profile != question.author:
        return JsonResponse({'error': 'Только автор вопроса может отмечать ответы'}, status=403)
    
    question.answer_set.update(is_correct=False)
    
    answer.is_correct = True
    answer.save()
    
    return JsonResponse({'status': 'ok'})
