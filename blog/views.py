from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.db.models import Max

from taggit.models import Tag

from accounts.models import UserProfile
from blog.models import Blog,BlogComment

from blog.forms import BlogPostForm

# Create your views here.


class PostListView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts=Blog.objects.filter(status=True)
        return posts    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        # context['longer featured blog']=Blog.objects.filter(status=True).order_by('-views','-publish_date').first()
        # v=Blog.objects.filter(status=True).order_by('-views','-publish_date').first()
        # print(v)
        # print(Blog.objects.filter(status=True).order_by('-views','-publish_date'))
        return context
    
    

class PostDetailView(DetailView):
    model = Blog
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.auther != self.request.user:
            session_key=f'viewed_article {self.object.slug}'
            if not self.request.session.get(session_key,False):
                self.object.views += 1
                self.object.save()
                self.request.session[session_key]=True
        context['comments']=BlogComment.objects.filter(post=kwargs['object'], parent=None)
        replies = BlogComment.objects.filter(post=kwargs['object']).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.comment_id not in replyDict.keys():
                replyDict[reply.parent.comment_id]=[reply]
            else:
                replyDict[reply.parent.comment_id].append(reply)

        context['replyDict']=replyDict
        context['total_blog_comment']=BlogComment.objects.filter(post=kwargs['object']).count()
        # print(Blog.objects.filter(tags__name__in=['django']))
        print(kwargs['object'].tags.all())
        context['tags']=kwargs['object'].tags.all()
        
        return context
    



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    form_class = BlogPostForm
    # fields = ['title','description','tags','image']
    template_name = 'blog/blog_post.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self,form):
        form.instance.auther=self.request.user
        form.instance.status=1
        return super().form_valid(form)



class PostCommentView(View):

    def post(self, request):
        comment = request.POST.get('comment')
        user = request.user
        post_slug=request.POST.get('post_slug')
        post=Blog.objects.get(slug=post_slug)
        parentId=request.POST.get('parentCommentId')
        if parentId=='':
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            # messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(comment_id=parentId)
            comment = BlogComment(comment=comment,user=user,post=post, parent=parent)
            comment.save()
            # messages.success(request, "Your reply has been posted successfully")
        return redirect(f"/{post.slug}/")


class DashboardView(LoginRequiredMixin,ListView):

    model = Blog
    context_object_name = 'publish_posts'
    template_name = 'blog/dashbord.html'

    def get_queryset(self):
        queryset = Blog.objects.filter(auther=self.request.user, status=True).order_by('publish_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft_post"] = Blog.objects.filter(auther=self.request.user, status=False)
        return context
    
    
