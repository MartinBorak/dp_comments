from django.conf.urls import include, url
from django.contrib import admin
from video.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^video/', include('video.urls')),
]
