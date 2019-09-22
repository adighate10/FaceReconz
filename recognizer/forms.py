from django import forms
from . import models


class CreateFaceData(forms.ModelForm):
    class Meta:
        model = models.FaceData
        fields = ['name', 'face_encoding', 'image_url' ]
        


class CreateRevealData(forms.ModelForm):
    class Meta:
        model = models.RevealData
        fields = ['image_url']
