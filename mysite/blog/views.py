from .models import Post, Comment
from .forms import CommentForm, UserUpdateForm
from django.views import generic, View
from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    

class AboutView(TemplateView):
    template_name = 'about.html'


class TutorialView(TemplateView):
    template_name = 'tutorials.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class PostDetailView(View):
    template_name = 'post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        return render(request, self.template_name, {'post': post, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(data=request.POST)
        new_comment = None
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return render(request, self.template_name, {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


class SignupView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html',{'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect(reverse('home'))


class LoginRequest(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'login_form':form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    if 'previous_pages' not in request.session:
                        request.session['previous_pages'] = []
                    previous_pages = request.session['previous_pages']
                    previous_pages.append(referer)
                    request.session['previous_pages'] = previous_pages
                    if len(previous_pages) >= 2:
                        return HttpResponseRedirect(previous_pages[-2])
                    else:
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
            else:
                messages.error(request,"Invalid username or password.")
                return render(request, 'login.html', {'form':form})
        else:
            messages.error(request,"Invalid username or password.")
            return render(request, 'login.html', {'form':form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/home/")


def delete_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = Comment.objects.filter(name=request.user.username).first()
            comment.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("You need to be logged in to delete a comment", status=405)


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = UserCreationForm()

    return render(request, 'cadmin/register.html', {'form': f})


def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)
        
        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'profile-update.html', context={'form': form})
    return redirect("home/")

