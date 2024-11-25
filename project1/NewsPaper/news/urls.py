from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPostsView

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # Добавлено имя
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/search/', SearchPostsView.as_view(), name='search_posts'),
]
