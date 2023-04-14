from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm

# Create your views here.

# READ All Movies (전체 영화 데이터 조회 및 index.html 렌더링)
def index(request):
    movies_list = Movie.objects.all() 
    context = {
        'movies_list': movies_list,
    }
    return render(request, 'movies/index.html', context)

# Read One Movies (단일 영화 데이터 조회 및 detail.html 렌더링)
def detail(request, pk):
    movies = Movie.objects.get(id=pk)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/detail.html', context) 

# CREATE (Create.html)
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES) # user가 입력한 데이터를 form에 채운다.
        if form.is_valid():                # 유효성 검사를 통과하면 
            movies = form.save()        # 데이터 저장 후 
            return redirect('movies:detail', movies.pk) # 상세 페이지로 redirect
    else:
        form = MovieForm()             # 비어있는 form을 만든다.
        
    context = {'form': form}
    return render(request, 'movies/create.html', context) # 유효성 검사를 통과하지 못하면 작성 페이지로 redirect

# DELETE (단일 영화 데이터 삭제 및 index.html 리다이렉트)
def delete(request, pk):
    movies = Movie.objects.get(id=pk)
    if request.method == 'POST':
        movies.delete()
        return redirect('movies:index')
    else:
        redirect('movies:detail', movies.pk)

# UPDATE (수정 대상 영화 데이터 조회 및 update.html 렌더링)
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