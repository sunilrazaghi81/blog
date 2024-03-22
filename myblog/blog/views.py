from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count




from taggit.models import Tag

from .models import *
from .forms import *


# PostListView

def list_post(request, tag_slug=None):  
    posts = Post.published.all()
    #taggit
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    #paginator
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    #Search
    if request.method == 'GET':
         q = request.GET.get('q')
         if q:
            vector = SearchVector('title', 'description')
            query = SearchQuery(q)
        
            s = Post.published.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
         else:
            s = None 
            

    context = {
        'posts':posts,
        's':s,
        'page':page,
        
    }
    return render(request, 'blog/list_post.html', context)



# DetailPostView

def detail_post(request, year, month, day, post):
    posts = get_object_or_404(Post, status="published", publish__year=year, publish__month=month,
                             publish__day=day, slug=post)
    
    post_tags_id = posts.tags.values_list('id', flat= True)
    similar_posts = Post.published.filter(tags__in = post_tags_id).exclude(id= posts.id)
    similar_posts = similar_posts.annotate(same_tags= Count('tags')).order_by('-same_tags', '-publish')
    
          
    # Comment Post  
    comments = posts.comment.filter(active=True)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = posts
            comment.save()
            return HttpResponseRedirect(request.path_info)
       
    else:
        form = CommentForm()
    context = {
        'posts': posts,
        'form':form,
        'comments':comments
    }
    return render(request, 'blog/detail_post.html', context)  
    

# CreatePostView
@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user  
            new_post.save()
            # This for added tags
            form.save_m2m()
            return redirect('blog:list') 
    else:
        form = PostForm()
    context = {
        'form':form,
        
    }
    return render(request, 'blog/create_post.html', context)


# DeletePostView

def delete_post(request, pk):
    posts = get_object_or_404(Post, id=pk)
    if request.user == posts.author:
        if request.method == 'POST':
            posts.delete()
            return redirect('blog:list')

        context = {
            'posts':posts,
            
        }
        return render(request, 'blog/delete_post.html', context)
    else:
        return HttpResponseForbidden()

# UpdatePostViwe

def update_post(request, pk):
    posts = get_object_or_404(Post, id=pk)
    if request.user == posts.author:
        form = PostUpdateForm(instance=posts)
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES, instance=posts)
            if form.is_valid():
                form.save()
            return redirect('blog:list')
        context = {
            'form':form,
            
        }
        return render(request, 'blog/update_post.html', context)
    else:
        return HttpResponseForbidden()


def about_me(request):
    return render(request, 'blog/about.html', {})