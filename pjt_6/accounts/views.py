from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.views.decorators.http import require_POST, require_safe, require_http_methods

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':   # request.method가 POST면 로그인 처리를 해줌
        form = AuthenticationForm(request, request.POST) 
        # 유저가 AuthenticationForm에 입력한 데이터를 가져와서 form에 담는다.
        if form.is_valid(): # form이 유효성 검사를 통과하면
            auth_login(request, form.get_user())
            return redirect('home:index')
    else:                          # request.method가 GET이면 비어있는 로그인 페이지를 구현해줌
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('home:index')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # 비어있는 폼이 아닌, request.POST에 들어있는 데이터가 채워진 폼
        if form.is_valid():                         # form에 있는 데이터가 유효성 검사를 통과하면  
            user = form.save()                      # 데이터 저장.
            auth_login(request, user)
            return redirect('home:index')
    else:
        form = CustomUserCreationForm()             # 비어있는 폼을 보여줌.
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['POST'])
def signout(request):
    user = request.user # 현재 request의 user를 가져오고, 
    user.delete() # user를 delete 
    auth.logout(request) # 로그아웃 처리 -> 해당 유저의 세션 정보 삭제 
    return redirect('home:index')

def update(request):
    # 로그인되어있는 상태가 아니면 메인 페이지로 redirect
    if not request.user.is_authenticated:
        return redirect('home:index')                  
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        # request에 들어 있는 user를 instance로 삼는다.
        # 'instance = request.user' 가 없으면 user가 입력한 데이터로 새 인스턴스를 생성하는 격.
        if form.is_valid():
            form.save()
            return redirect('home:index')
    else:                                     
        form = CustomUserChangeForm(instance = request.user)
        # request에 들어 있는 user를 instance로 삼는다. 
		# form = CustomerUserChangeForm() 라고만 적으면 비어있는 폼이 반환됨.
    context = {'form': form}
    return render(request, 'accounts/update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # session update 
            return redirect('home:index')
    else:
        form = PasswordChangeForm(request.user) 
        # request에 들어 있는 user를 instance로 삼는다. (비어있는 폼 반환 x)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)

def profile(request, username):
    user = get_user_model()
    person = User.objects.get(username=username)
    context = {'person': person}
    return render(request, 'accounts/profile.html', context)
