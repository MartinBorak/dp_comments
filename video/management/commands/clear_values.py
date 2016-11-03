from django.core.management.base import BaseCommand
from video.models import Comment, Reply


class Command(BaseCommand):
    help = "Clears all values in comments and replies."

    def handle(self, *args, **options):
        self.clear_comments()
        self.clear_replies()

    def clear_comments(self):
        comments = Comment.objects.all()

        for comment in comments:
            comment.reactions = 0
            comment.good = 0
            comment.neutral = 0
            comment.bad = 0
            comment.save()

    def clear_replies(self):
        replies = Reply.objects.all()

        for reply in replies:
            reply.reactions = 0
            reply.good = 0
            reply.neutral = 0
            reply.bad = 0
            reply.save()