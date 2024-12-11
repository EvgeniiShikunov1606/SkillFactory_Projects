from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from news.views import profile_view, CategoryDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('posts/', include('news.urls')),
    path('profile/', profile_view, name='profile'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', include('board.urls')),
]
