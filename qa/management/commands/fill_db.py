import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from qa.models import Profile, Tag, Question, Answer

fake = Faker()

class Command(BaseCommand):
    help = 'Заполняет бд тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Удаление старых данных'))
        clean_db()
        self.stdout.write(self.style.SUCCESS('Старые данные удалены'))

        ratio = kwargs['ratio']

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio} пользователей'))
        users = []
        for _ in range(ratio):
            user = User(username=fake.unique.user_name(), email=fake.email(), password='password123')
            users.append(user)
        User.objects.bulk_create(users)

        user_ids = [user.id for user in User.objects.all()]
        profiles = []
        for user_id in user_ids:
            profiles.append(Profile(user_id=user_id))
        Profile.objects.bulk_create(profiles)

        num_tags = ratio
        self.stdout.write(self.style.SUCCESS(f'Создание {num_tags} тэгов'))
        tags = []
        for _ in range(num_tags):
            tags.append(Tag(name=fake.unique.slug()))
        Tag.objects.bulk_create(tags)

        num_questions = ratio * 10
        self.stdout.write(self.style.SUCCESS(f'Создание {num_questions} вопросов'))
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        questions = []
        for _ in range(num_questions):
            question = Question(
                author_id=random.choice(profile_ids),
                title=fake.sentence(nb_words=5),
                text=fake.paragraph(nb_sentences=3),
            )
            questions.append(question)
        Question.objects.bulk_create(questions)

        all_questions = Question.objects.all()
        for question in all_questions:
            question.tags.set(random.sample(tag_ids, k=random.randint(1, 3)))
        
        num_answers = ratio * 100
        self.stdout.write(self.style.SUCCESS(f'Создание {num_answers} ответов'))
        question_ids = list(Question.objects.values_list('id', flat=True))

        answers = []
        for _ in range(num_answers):
            answer = Answer(
                author_id=random.choice(profile_ids),
                question_id=random.choice(question_ids),
                text=fake.paragraph(nb_sentences=2),
            )
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        self.stdout.write(self.style.SUCCESS('База данных заполнена'))

def clean_db():
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Tag.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()
