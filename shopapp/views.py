from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm as UserRegistrationForm, UpdateForm as UserProfileForm, PostForm, CommentForm
from .models import CustomUser as User, Post, Like, Comment
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

def index(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'posts': page_obj})

@login_required
def profile(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profile.html', {
        'user': user,
        'posts': page_obj
    })


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён.')
            return redirect('shopapp:profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'user_form.html', {'form': form})


@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Ваш профиль был удалён.')
        return redirect('shopapp:index')

    return render(request, 'delete_confirm_delete.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('shopapp:profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect('shopapp:profile')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shopapp:index')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'posts': page_obj})


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    return redirect('shopapp:post_detail', pk=pk)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('shopapp:index')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('shopapp:index')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост был успешно обновлён.')
            return redirect('shopapp:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})



def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('shopapp:index')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост был успешно удален.')
        return redirect('shopapp:index')

    return render(request, 'delete_post.html', {'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    if request.method == 'POST':
        # Если отправлен комментарий
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('shopapp:post_detail', pk=post.pk)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return redirect('shopapp:post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('shopapp:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('shopapp:post_detail', pk=post_pk)
    else:
        return redirect('shopapp:post_detail', pk=comment.post.pk)