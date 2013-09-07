from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from forum.forms import *


def default(request):

    return render(request, 'forum/default.html', {
        'categories': Category.objects.select_related('forum'),
        })


def forum(request, forum_slug):

    forum = get_object_or_404(Forum.objects.select_related(), slug=forum_slug)

    # Pagination of Topics
    paginator = Paginator(forum.topics.all(), 40)
    try:
        topics = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'forum/forum.html', {
        'forum': forum,
        'topics': topics,
        })


def topic(request, topic_id):

    topic = get_object_or_404(Topic.objects.select_related(), id=topic_id)

    # Pagination of Posts
    paginator = Paginator(topic.posts.all(), 25)
    try:
        posts = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Reply form
    if request.user.is_authenticated() and not topic.closed and request.method == 'POST':
        reply_form = PostForm(request.POST)
        if reply_form.is_valid():

            reply = reply_form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.author_ip = request.META['REMOTE_ADDR']
            reply.save()

            messages.success(request, "Your reply has been posted.")
            return redirect(reverse('forum_topic', kwargs={'topic_id': reply.topic.id}))

    elif request.user.is_authenticated() and not topic.closed:
        reply_form = PostForm()

    else:
        reply_form = None

    # Bump view counter
    topic.increment_view_count()

    return render(request, 'forum/topic.html', {
        'topic': topic,
        'posts': posts,
        'reply_form': reply_form,
        })


@login_required
def new_topic(request, forum_slug):

    forum = get_object_or_404(Forum, slug=forum_slug)

    # Starting a new Topic
    if request.method == 'POST':
        new_topic_form = TopicForm(request.POST)
        if new_topic_form.is_valid():

            # Create the new Topic
            new_topic = Topic(
                forum = forum,
                subject = new_topic_form.cleaned_data['subject'],
                author = request.user,
            )
            new_topic.save()

            # Create the new Post
            new_post = new_topic_form.save(commit=False)
            new_post.topic = new_topic
            new_post.author = request.user
            new_post.author_ip = request.META['REMOTE_ADDR']
            new_post.save()

            messages.success(request, "Your post has been saved.")
            return redirect(reverse('forum_topic', kwargs={'topic_id': new_topic.id}))

    elif request.user.is_authenticated():
        new_topic_form = TopicForm(initial={'forum': forum})

    else:
        new_topic_form = None

    return render(request, 'forum/new_topic.html', {
        'new_topic_form': new_topic_form,
        })


@login_required
def edit_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return HttpResponseForbidden()

    if post == post.topic.first_post:
        form = TopicForm
        initial = {
            'forum': post.topic.forum,
            'subject': post.topic.subject,
        }
    else:
        form = PostForm
        initial={}

    if request.method == 'POST':
        post_form = form(request.POST, instance=post)
        if post_form.is_valid():

            post = post_form.save(commit=False)
            post.updated = timezone.now()
            post.updated_by = request.user
            post.save()

            messages.success(request, "Your post has been updated.")
            return redirect(reverse('forum_topic', kwargs={'topic_id': post.topic.id}))

    else:
        post_form = form(instance=post, initial=initial)

    return render(request, 'forum/edit_post.html', {
        'post': post,
        'post_form': post_form,
        })