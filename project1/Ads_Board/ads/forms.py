from django import forms
from .models import AdsLetter, Ad


class AdsLetterForm(forms.ModelForm):
    class Meta:
        model = AdsLetter
        fields = ["subject", "message"]


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "category", "image1", "image2", "video1", "video2", "content"]
