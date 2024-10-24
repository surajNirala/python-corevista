from django.shortcuts import render
from .models import Post
from .forms import PostForm,UserRegistrationForm,CommentForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.http import JsonResponse

def index(request):
    return redirect('post_list')
    data = {}
    data['title'] = 'Post'
    return render(request, 'post/index.html',data)

def post_list(request):
    data = {}
    data['title'] = 'Post List'
    query = request.GET.get('search','')
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query) | Q(user__username__icontains=query)
            )
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON if it's an AJAX request
        post_data = []
        for post in posts:
            post_data.append({
                'id': post.id,
                'title': post.title,
                'text': post.text,
                'user': post.user.username,
                'photo': post.photo.url if post.photo else ''
            })
        return JsonResponse({'posts': post_data})
    # search
    data['posts'] = posts
    data['query'] = query
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
    data['form'] = form
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
            return render(request, 'registration/register.html', {'form': form})
    return render(request, 'registration/register.html',data)

def post_detail(request,post_id):
    data = {}
    data['title'] = 'Post detail'
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Link the comment to the post
            comment.user = request.user  # Set the user who made the comment
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to the same post after commenting
    else:
        form = CommentForm()
    data['post'] = post
    data['comments'] = post.comments.all().order_by('-created_at')
    data['form'] = form
    return render(request, 'post/post-detail.html', data)

    
