from django.conf.urls import url
from django.views.decorators.http import require_POST
from . import views

app_name = 'video'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^radio_form/(?P<comment_pk>[0-9]+)$', require_POST(views.radio_form_view), name='radio_form_view'),
    url(r'^leaderboard/$', views.LeaderBoardView.as_view(), name='leaderboard'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
]
