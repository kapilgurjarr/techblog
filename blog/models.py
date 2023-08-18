import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.utils import timezone

from taggit.managers import TaggableManager
from tinymce.models import HTMLField

# Create your models here.

STATUS = (
    (0,'Draft'),
    (1,'Publish')
)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = HTMLField(blank=True,null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    auther = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    likes = models.BigIntegerField(default=0)
    image = models.ImageField(upload_to='posts_images', blank=True, null=True)
    views = models.BigIntegerField(default=0)
    slug = models.SlugField(max_length=250,unique=True,blank=True)
    tags = TaggableManager()
    status = models.IntegerField(choices=STATUS,default=0)
    
    

    def save(self, *args, **kwargs):
        slug_sample = slugify(self.title)
        while Blog.objects.filter(slug=slug_sample).exists():
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
            slug_sample = slugify(self.title + ' ' + random_string)
        self.slug = slug_sample
        return super(Blog, self).save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50px" height="50px" />'%(self.image.url))
        else:
            return None
    image_tag.short_description = 'Image'
    
    

class BlogComment(models.Model):
    comment_id=models.BigAutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    comment_date= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username