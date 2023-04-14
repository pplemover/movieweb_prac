from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    # 단일 회원 프로필 조회
    path('profile/<str:username>/', views.profile, name='profile'),
]