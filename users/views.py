#user views

#Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,reverse
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


# Exception
from django.db.utils import IntegrityError


#models
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Post


#Forms
from users.forms import ProfileForm,SignupForm
# Create your views here.
class LoginView(auth_views.LoginView):
    template_name='users/login.html'


class SignupView(FormView):
    """Users sign up view."""

    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self,form):
        """save form data."""
        form.save()
        return super().form_valid(form)


class userDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})

"""update_profile another opcion
@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            url = reverse('users:detail',kwargs={'username':request.user.username})
            return redirect(url)

    else:
        form = ProfileForm()

    return render(
       request = request,
       template_name = 'users/update_profile.html',
       context={
       'profile':profile,
       'user':request.user,
       'form':form
    }
    )"""

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logged_out.html'
