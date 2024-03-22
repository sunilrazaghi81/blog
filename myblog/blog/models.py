from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField



# PublishedManager.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = "published")
   

# Post Model.

class Post(models.Model):
    
    STATUS = (
        ("draft", "Draft"), 
        ("published", "Published"),
    )
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    description = RichTextField()
    publish = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    image = models.ImageField(upload_to='image/%Y/%M/%D', null=False, blank=False)
    published = PublishedManager()
    tags = TaggableManager()
    
    def __str__(self):
         return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    class Meta:
        ordering = ('-publish',)
        

            
# Comment Model

class Comment(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comments_posts")
        name = models.CharField(max_length=100)
        comment = models.TextField()
        active = models.BooleanField(default=True)
        create = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            return self.name
        
        class Meta:
            ordering = ('-create',)