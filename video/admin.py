from django.contrib import admin
from .models import Video, Comment, Reply, Worker

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Worker)
