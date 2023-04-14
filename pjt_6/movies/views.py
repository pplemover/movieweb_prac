from django.shortcuts import render, redirect
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
# yj added
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required  
# Create your views here.

# READ All Movies (전체 영화 데이터 조회 및 index.html 렌더링)
@require_safe
def index(request):
    movies_list = Movie.objects.all() 
    context = {
        'movies_list': movies_list,
    }
    return render(request, 'movies/index.html', context)

# Read One Movies (단일 영화 데이터 조회 및 detail.html 렌더링)
@require_safe
def detail(request, pk):
    movies = Movie.objects.get(id=pk)
    comment_form = CommentForm()
    comments = movies.comment_set.all()
    re_comment_list = movies.comment_set.filter(parent__isnull=True) # 대댓글 리스트
    context = {
        'movies': movies,
        'comment_form': comment_form,
        'comments': comments,
        're_comment_list': re_comment_list,
    }
    return render(request, 'movies/detail.html', context) 

# CREATE (Create.html)
@require_http_methods(['GET', 'POST'])
@login_required
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES) # user가 입력한 데이터를 form에 채운다.
        if form.is_valid():                # 유효성 검사를 통과하면 
            movies = form.save(commit=False)        # 데이터 저장 후 
            movies.user = request.user
            movies.save()
            return redirect('movies:detail', movies.pk) # 상세 페이지로 redirect
    else:
        form = MovieForm()             # 비어있는 form을 만든다.
        
    context = {'form': form}
    return render(request, 'movies/create.html', context) # 유효성 검사를 통과하지 못하면 작성 페이지로 redirect

# DELETE (단일 영화 데이터 삭제 및 index.html 리다이렉트)
@require_POST
@login_required
def delete(request, pk):
    movies = Movie.objects.get(id=pk)
    if request.method == 'POST':
        movies.delete()
        return redirect('movies:index')
    else:
        redirect('movies:detail', movies.pk)

# UPDATE (수정 대상 영화 데이터 조회 및 update.html 렌더링)
@require_http_methods(['GET', 'POST'])
@login_required
def update(request, pk):
    movies = Movie.objects.get(id=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance = movies) # instance 인자로 수정 대상이 되는 객체를 지정
        if form.is_valid(): # 유효성 검사를 통과하면
            form.save()     # 데이터 저장
            return redirect('movies:detail', pk=movies.pk)
    else:
        form = MovieForm(instance=movies) # 기존 Movies 데이터를 채운 form

    context = {'movies': movies, 'form': form,}
    return render(request, 'movies/update.html', context)

@require_POST
@login_required
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        parent_pk = request.POST.get('parent_pk')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            if parent_pk: # 답글
                parent_comment = Comment.objects.get(pk=parent_pk)
                comment.parent = parent_comment
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

@require_POST
@login_required
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk = comment_pk)
        if request.user == comment.user:
            comment.delete()    
        return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')