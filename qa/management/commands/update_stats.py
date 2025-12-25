from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from qa.models import Tag, User, Question

class Command(BaseCommand):
    help = 'Recalculate popular tags and best users'

    def handle(self, *args, **kwargs):
        three_months_ago = timezone.now() - timedelta(days=90)
        
        popular_tags = Tag.objects.filter(
            question__created_at__gte=three_months_ago
        ).annotate(
            num_questions=Count('question')
        ).order_by('-num_questions')[:10]
        
        if not popular_tags:
            popular_tags = Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:10]

        cache.set('popular_tags', list(popular_tags), 3600 * 24)

        one_week_ago = timezone.now() - timedelta(days=7)
        
        best_users_ids = Question.objects.filter(
            created_at__gte=one_week_ago
        ).order_by('-rating').values_list('author__user', flat=True)[:10]
        
        if not best_users_ids:
             users = User.objects.all()[:10]
        else:
             users = User.objects.filter(id__in=best_users_ids)
        
        cache.set('best_users', list(users), 3600 * 24)

        self.stdout.write(self.style.SUCCESS('Successfully updated stats'))
        