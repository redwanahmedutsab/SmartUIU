import json

from django.http import JsonResponse
from django.utils import timezone
from .models import Comment, Reply, Tag, LikeDislike
from .forms import CommentForm, ReplyForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.contrib.auth.decorators import login_required
from django import forms


@login_required(login_url='/login')
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)

    if comment.author == request.user:
        comment.delete()

    return redirect('blog_single', id=comment.blog.id)


@login_required(login_url='/login')
def reply_delete(request, id):
    reply = get_object_or_404(Reply, id=id)

    if reply.author == request.user:
        reply.delete()

    return redirect('blog_single', id=reply.comment.blog.id)


@login_required(login_url='/login')
def blog_single_view(request, id):
    blog = get_object_or_404(Blog, id=id)
    like = blog.reactions.filter(reaction='like').count()
    dislike = blog.reactions.filter(reaction='dislike').count()
    user_reaction = blog.reactions.filter(user=request.user).first()

    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.author = request.user
                comment.save()
                return redirect('blog_single', id=blog.id)

        elif 'submit_reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment = get_object_or_404(Comment, id=request.POST['comment_id'])
                reply.author = request.user
                reply.save()
                return redirect('blog_single', id=blog.id)

        elif 'submit_nested_reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                parent_reply = get_object_or_404(Reply, id=request.POST['reply_id'])
                nested_reply = reply_form.save(commit=False)
                nested_reply.comment = parent_reply.comment  # Link to the same comment
                nested_reply.parent_reply = parent_reply  # Set parent reply
                nested_reply.author = request.user
                nested_reply.save()
                return redirect('blog_single', id=blog.id)

    else:
        comment_form = CommentForm()
        reply_form = ReplyForm()

    context = {
        'blog': blog,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'like': like,
        'dislike': dislike,
        'user_reaction': user_reaction,
    }

    return render(request, 'blog/blog_single.html', context)


@login_required(login_url='/login')
def home(request):
    search_term = request.GET.get('search', '')
    sort_order = request.GET.get('sort', '')
    specific_date = request.GET.get('specific_date')

    blogs = Blog.objects.all().order_by('-created_at')

    if search_term:
        blogs = blogs.filter(title__icontains=search_term) | blogs.filter(tags__name__icontains=search_term)

    if specific_date:
        blogs = blogs.filter(created_at__startswith=specific_date)

    if sort_order == 'new_to_old':
        blogs = blogs.order_by('-created_at')
    elif sort_order == 'old_to_new':
        blogs = blogs.order_by('created_at')

    blogs_count = blogs.count()

    return render(request, 'blog/blog.html', {
        'blogs': blogs,
        'search_term': search_term,
        'sort_order': sort_order,
        'specific_date': specific_date,
        'blogs_count': blogs_count,
    })


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
    return render(request, 'blog/blog.html', {'blog': blog})


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

        new_tags = request.POST.get('new_tags', '')
        if new_tags:
            tag_names = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        return redirect('blog')

    return render(request, 'blog/blog_post.html')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'photo']


@login_required(login_url='/login')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')

        new_tags = request.POST.get('new_tags')
        tag_names = [tag.strip() for tag in new_tags.split(',')]
        tag_objects = []
        for tag_name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag_obj)

        blog.tags.set(tag_objects)

        if request.FILES.get('photo'):
            blog.photo = request.FILES['photo']

        blog.save()

        return redirect('blog_my_blog')

    return render(request, 'blog/blog_edit.html', {'blog': blog})


@login_required(login_url='/login')
def toggle_reaction(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        data = json.loads(request.body)
        reaction_type = data.get('reaction_type')

        reaction = LikeDislike.objects.filter(blog=blog, user=request.user).first()

        if reaction:
            if reaction_type == 'like' and reaction.reaction == LikeDislike.Liked:
                reaction.delete()
                action = 'removed'
            elif reaction_type == 'dislike' and reaction.reaction == LikeDislike.Disliked:
                reaction.delete()
                action = 'removed'
            else:
                if reaction_type == 'like':
                    reaction.reaction = LikeDislike.Liked
                    action = 'toggled'
                elif reaction_type == 'dislike':
                    reaction.reaction = LikeDislike.Disliked
                    action = 'toggled'
                reaction.save()
        else:
            if reaction_type == 'like':
                LikeDislike.objects.create(blog=blog, user=request.user, reaction=LikeDislike.Liked)
                action = 'toggled'
            elif reaction_type == 'dislike':
                LikeDislike.objects.create(blog=blog, user=request.user, reaction=LikeDislike.Disliked)
                action = 'toggled'

        like_count = LikeDislike.objects.filter(blog=blog, reaction=LikeDislike.Liked).count()
        dislike_count = LikeDislike.objects.filter(blog=blog, reaction=LikeDislike.Disliked).count()

        return JsonResponse(
            {'blog_id': blog_id, 'like_count': like_count, 'dislike_count': dislike_count, 'action': action})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='/login')
def tag_search(request, tag_name):
    blog = Blog.objects.filter(tags__name__icontains=tag_name)
    return render(request, 'blog/blog_tag.html', {'blogs': blog, 'tag':tag_name})
