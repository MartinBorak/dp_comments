from django.core.management.base import BaseCommand
from video.models import Video, Author, Comment, Reply, Worker


class Command(BaseCommand):
    help = "Clears all values in comments and replies."

    def handle(self, *args, **options):
        self.clear_videos()
        self.clear_comments()
        self.clear_replies()
        self.clear_workers()

    def clear_videos(self):
        Video.objects.all().update(show=True)
        Video.objects.all().update(priority=0.0)

    def clear_comments(self):
        Comment.objects.all().update(reactions=0)
        Comment.objects.all().update(good=0)
        Comment.objects.all().update(neutral=0)
        Comment.objects.all().update(bad=0)
        Comment.objects.all().update(show=True)

    def clear_replies(self):
        Reply.objects.all().update(reactions=0)
        Reply.objects.all().update(good=0)
        Reply.objects.all().update(neutral=0)
        Reply.objects.all().update(bad=0)

    def clear_workers(self):
        Worker.objects.all().update(score=0)
        workers = Worker.objects.all()

        for worker in workers:
            worker.comments.clear()
            worker.videos.clear()
