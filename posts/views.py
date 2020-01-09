"""Posts views."""

# Django
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy

# Forms
from posts.forms import PostForm

# Models
from posts.models import Post


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 5
    context_object_name = 'posts'

class postDetailView(LoginRequiredMixin, DetailView):
    """postDetailView"""

    template_name='posts/detail.html'
    queryset =Post.objects.all()
    context_object_name='post'



class CreatePostView(LoginRequiredMixin,CreateView):
    template_name = "posts/new.html"
    success_url = reverse_lazy("posts:feed")
    form_class = PostForm

    def get_context_data(self,**kwargs):
        """Add user and profile to context."""
        context =  super().get_context_data(**kwargs)
        context['users'] = self.request.user
        context['profile']= self.request.user.profile
        return context
