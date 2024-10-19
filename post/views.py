from django.shortcuts import render
from .models import Post
from .forms import PostForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def index(request):
    data = {}
    data['title'] = 'Post'
    return render(request, 'post/index.html',data)

def post_list(request):
    data = {}
    data['title'] = 'Post List'
    posts = Post.objects.all().order_by('-created_at')
    data['posts'] = posts
    return render(request, 'post/post-list.html',data)

@login_required
def post_create(request):
    data = {}
    data['title'] = 'Create Post'    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('post_list')
    else:
        data['form'] = PostForm()
    return render(request, 'post/post-form.html',data)

@login_required
def post_edit(request,post_id):
    data = {}
    data['title'] = 'Edit Post'
    post = get_object_or_404(Post,pk=post_id,user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post-form.html',data)

@login_required
def post_delete(request,post_id):
    data = {}
    data['title'] = 'Delete  Post'
    post = get_object_or_404(Post,pk=post_id,user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    data['post'] = post
    return render(request, 'post/post-confirm-delete.html',data)

def register(request):
    data = {}
    data['title'] = 'User Register'
    data['form'] = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)      
            return redirect('post_list')
        else:
            data['error'] = "Invalid form data"
    return render(request, 'registration/register.html',data)

    
