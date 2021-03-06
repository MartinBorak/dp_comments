from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    video_id = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=500)
    show = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)


class Author(models.Model):
    author_id = models.CharField(max_length=100)
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=100, default='')
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    reactions = models.IntegerField(default=0)
    show = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    def clear(self):
        self.reactions = 0
        self.good = 0
        self.neutral = 0
        self.bad = 0
        self.save()


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_id = models.CharField(max_length=100, default='')
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    reactions = models.IntegerField(default=0)
    published_at = models.DateTimeField(default=None)
    show = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    def clear(self):
        self.reactions = 0
        self.good = 0
        self.neutral = 0
        self.bad = 0
        self.save()

    class Meta:
        ordering = ['published_at']


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video)
    comments = models.ManyToManyField(Comment)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

User.worker = property(lambda u:Worker.objects.get_or_create(user=u)[0])
