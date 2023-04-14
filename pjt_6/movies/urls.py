from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # READ1 (전체 영화 목록 페이지 조회)
    path('', views.index, name='index'),
    # READ2 (단일 영화 목록 페이지 조회)
    path('<int:pk>/', views.detail, name='detail'),

    # CREATE(새로운 영화 생성 페이지 조회 & 단일 영화 데이터 저장)
    path('create/', views.create, name='create'),

    # DELETE (단일 영화 데이터 삭제)
    path('<int:pk>/delete/', views.delete, name='delete'),

    # UPDATE (기존 영화 수정 페이지 조회 & 단일 영화 데이터 수정)
    path('<int:pk>/update/', views.update, name='update'),


    # Comment CREATE (댓글 생성)
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),

    # Comment DELETE (댓글 삭제)
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),

    # Comment (댓글 생성)
    # path('<int:pk>/comments/', views.comments_create, name='comments_create')
]
