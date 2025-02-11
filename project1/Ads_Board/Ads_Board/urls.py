"""
URL configuration for AdsBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ads.views import (AdViewSet, ResponseViewSet, UserResponsesListView,
                        ads_list, ad_detail, response_list, accept_response, delete_response,
                        send_ads_letter, AdCreate)
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('ads.urls')),
    path("", ads_list, name="ads_list"),
    path("ad/<int:ad_id>/", ad_detail, name="ad_detail"),
    path("responses/", response_list, name="response_list"),
    path("response/<int:response_id>/accept/", accept_response, name="accept_response"),
    path("response/<int:response_id>/delete/", delete_response, name="delete_response"),
    path("ads_letter/", send_ads_letter, name="send_ads_letter"),
    path("ads_letter/success/", TemplateView.as_view(template_name="ads/ads_letter_success.html"),
         name="ads_letter_success"),
    path('add_ad/', AdCreate.as_view(), name='ad_form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
