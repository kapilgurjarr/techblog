from django.contrib import admin
from blog.models import Blog,BlogComment
from django.urls import reverse

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','auther','publish_date','update_date','status','image_tag']
    # exclude = ['slug','description']
    search_fields = ['title','auther']
    fields = ('auther','title','slug','description','image','tags','status','views')
    list_filter = ['tags','publish_date','status']

    
admin.site.register(BlogComment)
