from django.db import models
import os
from uuid import uuid4
from PIL import Image, ImageDraw, ImageFont
import face_recognition
from io import BytesIO
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.


def content_file_name(instance, filename):
    upload_to = ''+instance.name
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        filename = '{}.{}'.format(instance.name, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def revealFace_file_name(instance, filename):
    upload_to = ''+"reveal"
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("reveal", ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class FaceData(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.TextField(default = "facereconz")
    image_url = models.ImageField(
        default='default.png', blank=True, upload_to=content_file_name)

class RevealData(models.Model):
    name = models.CharField(max_length=100, default='default')
    age_group = models.CharField(max_length=100, default='undetected')
    image_url = models.ImageField(
        default='default.png', blank=True, upload_to=revealFace_file_name)



