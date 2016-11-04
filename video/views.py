import random
from django.db.models import F
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Video, Comment, Worker, Author
from .forms import RegisterForm, RadioForm


class IndexView(generic.ListView):
    template_name = 'video/index.html'
    context_object_name = 'all_videos'

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated():
            user_videos = user.worker.videos.all()
            main_set = Video.objects.filter(show=True).exclude(pk__in=user_videos).order_by('-priority')
        else:
            main_set = Video.objects.filter(show=True).order_by('-priority')

        # subset = [main_set[i] for i in sorted(random.sample(range(len(main_set)), 10))]
        subset = main_set[:10]

        return subset


class DetailView(generic.DetailView):
    model = Video
    template_name = 'video/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated():
            user_comments = user.worker.comments.all()
            comments = context['object'].comment_set.filter(show=True).exclude(pk__in=user_comments)
        else:
            comments = context['object'].comment_set.filter(show=True)

        context['comments'] = [comments[i] for i in sorted(random.sample(range(len(comments)), 1))]
        context['form'] = RadioForm(reply_count=len(context['comments'][0].reply_set.all()))

        return context


def radio_form_view(request, comment_pk=0):
    reply_count = len(request.POST) - 2
    form = RadioForm(request.POST or None, reply_count=reply_count)

    values = []

    if form.is_valid():
        values.append(str(form.cleaned_data['comment_radio']))

        for i in range(0, reply_count):
            values.append(str(form.cleaned_data['reply_' + str(i)]))

    comment = Comment.objects.get(pk=comment_pk)
    video = comment.video
    replies = comment.reply_set.all()

    if values[0] == 'opt0':
        comment.good += 1
    elif values[0] == 'opt1':
        comment.neutral += 1
    elif values[0] == 'opt2':
        comment.bad += 1
    else:
        return redirect('video:index')

    comment.reactions += 1

    # SET WORKER SCORE
    worker = request.user.worker
    worker.comments.add(comment)
    worker.score += 2 + comment.reply_set.count()

    comment_set = video.comment_set.all()

    is_all = True

    for c in comment_set:
        if c not in worker.comments.all():
            is_all = False
            break

    if is_all:
        worker.videos.add(video)
        worker.score += 5

    worker.save()

    # DO NOT DISPLAY COMMENTS WITH MORE THAN 3 REACTIONS
    if comment.reactions >= 3:
        comment.show = False

        author = comment.author
        authors_comments = author.comment_set.all()
        authors_replies = author.reply_set.all()
        author_videos = []

        for c in authors_comments:
            author_videos.append(c.video.pk)

        for r in authors_replies:
            author_videos.append(r.comment.video.pk)

        Video.objects.filter(pk__in=author_videos).update(priority=F('priority') - 3)

        comment.reply_set.update(show=False)

        for rep in comment.reply_set.all():
            author = rep.author
            authors_comments = author.comment_set.all()
            authors_replies = author.reply_set.all()
            author_videos = []

            for c in authors_comments:
                author_videos.append(c.video.pk)

            for r in authors_replies:
                author_videos.append(r.comment.video.pk)

            Video.objects.filter(pk__in=author_videos).update(priority=F('priority') - 3)

        show_set = video.comment_set.filter(show=True)

        if not show_set:
            video.show = False
            video.save()

    comment.save()

    # INCREASE PRIORITY OF VIDEOS WITH AUTHOR
    author = comment.author
    authors_comments = author.comment_set.all()
    authors_replies = author.reply_set.all()
    author_videos = []

    for c in authors_comments:
        author_videos.append(c.video.pk)

    for r in authors_replies:
        author_videos.append(r.comment.video.pk)

    Video.objects.filter(pk__in=author_videos).update(priority=F('priority') + 1)

    i = 1

    for reply in replies:
        if values[i] == 'opt0':
            reply.good += 1
        elif values[i] == 'opt1':
            reply.neutral += 1
        elif values[i] == 'opt2':
            reply.bad += 1
        else:
            return redirect('video:index')

        reply.reactions += 1
        replies[i - 1].save()

        author = reply.author
        authors_comments = author.comment_set.all()
        authors_replies = author.reply_set.all()
        author_videos = []

        for c in authors_comments:
            author_videos.append(c.video.pk)

        for r in authors_replies:
            author_videos.append(r.comment.video.pk)

        Video.objects.filter(pk__in=author_videos).update(priority=F('priority') + 1)

        i += 1

    return redirect('video:index')


class UserRegisterView(View):
    form_class = RegisterForm
    template_name = 'video/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('video:index')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    template_name = 'video/login_form.html'

    def get(self, request):
        auth_form = AuthenticationForm(None, request.POST or None)
        return render(request, self.template_name, {'form': auth_form})

    def post(self, request):
        auth_form = AuthenticationForm(None, request.POST or None)

        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect('video:index')

        return render(request, self.template_name, {'form': auth_form, 'error_message': 'Incorrect username or password'})


def logout_view(request):
    logout(request)
    return redirect('video:login')


class LeaderBoardView(generic.ListView):
    template_name = 'video/leaderboard.html'
    context_object_name = 'workers'

    def get_queryset(self):
        main_set = Worker.objects.all().order_by('-score')
        subset = main_set[0:10]

        return subset


class ProfileView(generic.TemplateView):
    template_name = 'video/profile.html'
