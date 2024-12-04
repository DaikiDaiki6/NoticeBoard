from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from httpx import delete
from .models import *
from bs4 import BeautifulSoup
import requests
from httpx import delete
from django.contrib import messages
from .forms import *

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
        
    categories = Tag.objects.all()
    
    context = {
        'posts':posts,
        'categories': categories,
        'tag' : tag
    }
    return render(request, 'a_posts/home.html', context)

@login_required
def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('home')
        
    return render(request, 'a_posts/post_create.html', {'form': form})


@login_required
def post_delete_view(request, pk):
    if request.user.is_staff:
        post = get_object_or_404(Post, id=pk)
    else:
        post = get_object_or_404(Post, id=pk, author = request.user)
    if request.method == "POST":
        post.delete()
        if request.user.is_staff:
            messages.success(request, 'Admin: Notice Deleted')
        else:
            messages.success(request, 'Notice Deleted')
        return redirect('home')
    
    return render(request, 'a_posts/post_delete.html', {'post': post})  # Render confirmation page.


def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author = request.user)
    form = PostEditForm(instance=post)  
    
    if request.method == "POST":
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated')
            
            return redirect('home')

            
    context = {
        'post':post,
        'form':form
    }          
    return render(request, 'a_posts/post_edit.html', context)  # Render confirmation page.
    

def post_page_view(request, pk):
    #post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    
    context = {
        'post': post,
        'commentform': commentform,
        'replyform' : replyform
    }
    
    return render(request, 'a_posts/post_page.html', context)  # Render confirmation page.

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
    return redirect('post', post.id)

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author = request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Comment Deleted')
        
        return redirect('post', post.parent_post.id)
    
    return render(request, 'a_posts/comment_delete.html', {'comment': post})  # Render confirmation page.

@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            
    return redirect('post', comment.parent_post.id)

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author = request.user)
    
    if request.method == "POST":
        reply.delete()
        messages.success(request, 'Reply Deleted')
        
        return redirect('post', reply.parent_comment.parent_post.id)
    
    return render(request, 'a_posts/reply_delete.html', {'reply': reply})  # Render confirmation page.

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exist = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return redirect('post', post.id)

def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    user_exist = comment.likes.filter(username=request.user.username).exists()

    if comment.author != request.user:
        if user_exist:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

    return redirect('post', pk=comment.parent_post.id)

def like_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    user_exist = reply.likes.filter(username=request.user.username).exists()

    if reply.author != request.user:
        if user_exist:
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)

    return redirect('post', pk=reply.parent_comment.parent_post.id)
