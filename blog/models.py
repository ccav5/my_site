from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
#自定义管理器
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title =  models.CharField(max_length =250)
    #'url'的单位 ‘-’
    slug = models.SlugField(max_length=250,unique_for_date = 'publish')
    # 多个学生对应一个教师，通过主表查询子表可以用字表的名称小写加上_set,或者是在定义外键的时候传入参数related_name，teacher.sutdent_set.all()=teacher.sudent_teacher.all()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=models.Manager()
    published=PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return ' Comments by {} on {}'.format(self.name,self.post)








