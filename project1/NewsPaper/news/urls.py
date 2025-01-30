from django.urls import path, include
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPostsView, subscribe_to_category, \
    CategoryDetailView, TaskView
from django.views.decorators.cache import cache_page
from django.urls import path


urlpatterns = [
    path('', cache_page(60*1)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchPostsView.as_view(), name='post_search'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
    path('task/<int:post_id>/', TaskView.as_view(), name='task'),
    path('i18n/', include('django.conf.urls.i18n')),
]
