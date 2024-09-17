from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import CommentForm, ReplyForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.contrib.auth.decorators import login_required
from django import forms


@login_required(login_url='/login')
def blog_single_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        # Handle comment submission
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.author = request.user
                comment.save()
                return redirect('blog_single', id=blog.id)

        # Handle reply submission
        elif 'submit_reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment = Comment.objects.get(id=request.POST['comment_id'])
                reply.author = request.user
                reply.save()
                return redirect('blog_single', id=blog.id)

    else:
        comment_form = CommentForm()
        reply_form = ReplyForm()

    context = {
        'blog': blog,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }

    return render(request, 'blog/blog_single.html', context)


@login_required(login_url='/login')
def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog.html', {'blogs': blogs})


@login_required(login_url='/login')
def blog_my_blog_view(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'blog/blog_my_blog.html', {'blogs': blogs})


@login_required(login_url='/login')
def blog_delete_view(request, id):
    blog = get_object_or_404(Blog, id=id, author=request.user)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('blog_my_blog')
    return render(request, 'blog/blog_delete_confirm.html', {'blog': blog})


@login_required(login_url='/login')
def blog_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        photo = request.FILES.get('photo')
        author = request.user

        blog = Blog(
            title=title,
            content=content,
            photo=photo,
            author=author,
            created_at=timezone.now(),
        )
        blog.save()

        return redirect('blog')

    return render(request, 'blog/blog_post.html')


# Blog edit form
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'photo']


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_my_blog')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blog/blog_edit.html', {'form': form, 'blog': blog})
