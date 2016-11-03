from django.core.management.base import BaseCommand
from video.models import Comment, Reply


class Command(BaseCommand):
    help = "Clears all values in comments and replies."

    def handle(self, *args, **options):
        self.clear_comments()
        self.clear_replies()

    def clear_comments(self):
        Comment.objects.all().update(reactions=0)
        Comment.objects.all().update(good=0)
        Comment.objects.all().update(neutral=0)
        Comment.objects.all().update(bad=0)

    def clear_replies(self):
        Reply.objects.all().update(reactions=0)
        Reply.objects.all().update(good=0)
        Reply.objects.all().update(neutral=0)
        Reply.objects.all().update(bad=0)
