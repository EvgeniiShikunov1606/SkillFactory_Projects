from rest_framework import viewsets, permissions
from .models import Ad, Response
from .serializers import AdSerializer, ResponseSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import AdsLetterForm, AdForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all().order_by("-created_at")
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        response = serializer.save(author=self.request.user)
        ad_author_email = response.ad.author.email

        if ad_author_email:
            send_mail(
                subject=f"Новый отклик на ваше объявление: {response.ad.title}",
                message=f"Пользователь {response.author.username} оставил отклик:\n\n{response.text}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[ad_author_email],
                fail_silently=False,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        response = self.get_object()

        if response.ad.author != request.user:
            return Response({"error": "Вы не можете принять этот отклик"}, status=403)

        response.accepted = True
        response.save()

        send_mail(
            subject="Ваш отклик принят!",
            message=f"Поздравляем! Ваш отклик на объявление '{response.ad.title}' был принят.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email],
            fail_silently=False,
        )

        return DRFResponse({"message": "Отклик принят!"})

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        response = self.get_object()
        user = request.user

        if response.ad.author != user and response.author != user:
            return Response({"error": "Вы не можете удалить этот отклик"}, status=403)

        if user == response.author:
            subject = "Ваш отклик удалён"
            message = f"Вы удалили свой отклик на объявление '{response.ad.title}'."
        else:
            subject = "К сожалению, ваш отклик был удалён"
            message = f"К сожалению, ваш отклик на объявление '{response.ad.title}' был удалён владельцем объявления."

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email],
            fail_silently=False,
        )

        response.delete()
        return Response({"message": "Отклик удалён"})


class UserResponsesListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Response.objects.filter(ad__author=self.request.user).order_by("-created_at")


def ads_list(request):
    ads = Ad.objects.all().order_by("-created_at")
    return render(request, "ads/ads_list.html", {"ads": ads})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    responses = Response.objects.filter(ad=ad)

    if request.method == "POST":
        text = request.POST.get("text")
        if text and request.user.is_authenticated:
            Response.objects.create(ad=ad, author=request.user, text=text)
            return redirect("ad_detail", ad_id=ad.id)

    return render(request, "ads/ad_detail.html", {"ad": ad, "responses": responses})


@login_required
def response_list(request):
    ads = Ad.objects.filter(author=request.user)
    selected_ad_id = request.GET.get("ad_id")

    if selected_ad_id:
        responses = Response.objects.filter(ad__id=selected_ad_id, ad__author=request.user)
    else:
        responses = Response.objects.filter(ad__author=request.user)

    return render(
        request,
        "ads/response_list.html",
        {"ads": ads, "responses": responses, "selected_ad_id": selected_ad_id},
    )


@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, ad__author=request.user)
    response.accepted = True
    response.save()

    send_mail(
        subject="Ваш отклик принят!",
        message=f"Поздравляем! Ваш отклик на объявление '{response.ad.title}' был принят.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email],
        fail_silently=False,
    )

    return HttpResponseRedirect(reverse("response_list"))


@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, ad__author=request.user)

    send_mail(
        subject="Ваш отклик был удалён",
        message=f"К сожалению, ваш отклик на объявление '{response.ad.title}' был удалён.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email],
        fail_silently=False,
    )

    response.delete()
    return HttpResponseRedirect(reverse("response_list"))


@staff_member_required
def send_ads_letter(request):
    if request.method == "POST":
        form = AdsLetterForm(request.POST)
        if form.is_valid():
            ads_letter = form.save()

            recipient_list = User.objects.values_list("email", flat=True)

            send_mail(
                subject=ads_letter.subject,
                message=ads_letter.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=list(recipient_list),
                fail_silently=False,
            )

            return redirect("ads_letter_success")

    else:
        form = AdsLetterForm()

    return render(request, "ads/send_ads_letter.html", {"form": form})


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'ads/ad_create.html'
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)

    def photo_upload(self):
        if self.method == 'POST':
            form = AdForm(self.POST, self.FILES)
            if form.is_valid():
                form.save()
                return redirect('photo_list')
        else:
            form = AdForm()
        return render(self, 'ads/ad_create.html', {'form': form})

    def photo_list(self):
        photos = Ad.objects.all()
        return render(self, 'ads/ad_create.html', {'photos': photos})


class AdUpdate(UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'ads/ad_update.html'
    success_url = reverse_lazy('ads_list')

    def dispatch(self, request, *args, **kwargs):
        ad = self.get_object()
        if ad.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdDelete(DeleteView):
    model = Ad
    template_name = 'ads/ad_delete.html'
    success_url = reverse_lazy('ads_list')

    def dispatch(self, request, *args, **kwargs):
        ad = self.get_object()
        if ad.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


