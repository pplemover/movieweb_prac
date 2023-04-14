from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST, require_safe, require_http_methods

from .models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index') 
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['POST'])
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index') 
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)

@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index') 
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)

def profile(request, username):
    User = get_user_model() # get_user_model()로 활성화되어 있는 User 모델을 가져온다. 
    person = User.objects.get(username=username) # 인자로 넘어온 username으로 User 인스턴스를 person에 할당한다. 
    context = {'person': person}
    return render(request, 'accounts/profile.html', context)

@require_http_methods(['POST'])
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_user_model().objects.get(pk=user_pk) # 클릭하여 선택한 유저정보를 person에 담는다. 
        # 만약 선택한 유저정보가 나 자신이라면 follow 가 되면 안됨. 선택한 유저가 나 자신과 다를 때에서만 로직 구동.
        if person != request.user: 
            if person.followers.filter(pk=request.user.pk).exists(): # 선택한 유저를 팔로우한 사람들 중 내가 있다면, 
            # if request.user in person.followers.all() 
                person.followers.remove(request.user)                # followers 목록에서 나를 지운다. 
            else:                                                    # 선택한 유저플 팔로우한 사람들 중 내가 없다면,
                person.followers.add(request.user)                   # followers 목록에 나를 추가한다.
        return redirect('accounts:profile', person.username)
    return redirect('accounts:login')