from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from django_bleach.models import BleachField


class Category(models.Model):
    name = models.CharField('Name', max_length=80)
    position = models.PositiveSmallIntegerField('Position', default=0)

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums')
    name = models.CharField('Name', max_length=80)
    slug = models.SlugField('Slug', max_length=80, editable=False)
    position = models.PositiveSmallIntegerField('Position', default=0)
    description = models.TextField('Description', blank=True, default='')
    updated = models.DateTimeField('Updated', auto_now=True)
    post_count = models.IntegerField('Post count', blank=True, default=0, editable=False)
    topic_count = models.IntegerField('Topic count', blank=True, default=0, editable=False)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum_forum', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def update_counters(self):
        posts = Post.objects.filter(topic__forum_id=self.id)
        self.post_count = posts.count()
        self.topic_count = Topic.objects.filter(forum_id=self.id).count()
        try:
            last_post = posts.order_by('-created')[0]
            self.updated = last_post.updated or last_post.created
        except IndexError:
            pass
        self.save()


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics')
    subject = models.CharField('Subject', max_length=255)
    author = models.ForeignKey(User, related_name='topics', editable=False)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', null=True, editable=False)
    sticky = models.BooleanField('Sticky', blank=True, default=False)
    closed = models.BooleanField('Closed', blank=True, default=False)
    view_count = models.PositiveIntegerField('Views count', blank=True, default=0, editable=False)
    reply_count = models.IntegerField('Reply count', blank=True, default=0, editable=False)
    last_reply = models.ForeignKey('Post', related_name='last_in_topic', blank=True, null=True, editable=False)

    class Meta:
        ordering = ['sticky', '-updated']
        get_latest_by = 'updated'

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('forum_topic', kwargs={'topic_id': self.id})

    def update_counters(self):
        # Set pointer to most recent Post in Topic
        last_post = Post.objects.filter(topic_id=self.id).order_by('-created')[0]
        self.updated = last_post.updated or last_post.created
        # Count replies
        self.reply_count = self.posts.count() - 1 # Initial post doesn't count
        if self.reply_count:
            self.last_reply = last_post
        self.save()

    def increment_view_count(self):
        self.view_count +=1
        self.save()

    def _first_post(self):
        return self.posts.order_by('created')[0]
    first_post = property(_first_post)


class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts')
    author = models.ForeignKey(User, related_name='posts', editable=False)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(User, verbose_name='Updated by', blank=True, null=True, editable=False)
    author_ip = models.GenericIPAddressField('Author IP', blank=True, null=True)
    body = BleachField()

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        # Update Topic and Forum counter
        self.topic.update_counters()
        self.topic.forum.update_counters()
