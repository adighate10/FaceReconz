from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FaceData, RevealData
from . import forms
import face_recognition
from PIL import Image, ImageDraw
import os
from django.conf import settings

# Create your views here.

def crosssite(request):
	id = request.GET.get('id','')
	return HttpResponse('Hello User %s'%id)


def index(request):
	#return HttpResponse('Hello User')
	return render (request, 'recognizer/index.html')

def train_model(request):
	if request.method == 'POST':
		form = forms.CreateFaceData(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			#design train successfull page
			known_image = face_recognition.load_image_file(instance.image_url)
			face_encoding = face_recognition.face_encodings(known_image)[0]
			instance.face_encoding = face_encoding;
			instance.save()
			return redirect('recognizer:reveal')	
	else:
		form = forms.CreateFaceData()
	return render(request, 'recognizer/train_model.html', { 'form': form })


def reveal_faces(request):
	if request.method == 'POST':
		form = forms.CreateRevealData(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			#design train successfull page
			return redirect('recognizer:reveal_results')
		else:
			form = forms.CreateRevealData()
	else:
		form = forms.CreateRevealData()
	return render(request, 'recognizer/reveal_faces.html', {'form': form})

def reveal_results(request):
			image_path = os.path.join(settings.MEDIA_ROOT , os.path.join("reveal", "reveal.jpg"))
			image_url = os.path.join(settings.MEDIA_URL , os.path.join("reveal", "reveal.jpg"))
			unknown_image = face_recognition.load_image_file(image_path)
			img = Image.fromarray(unknown_image)
			img_draw = ImageDraw.Draw(img)
			face_locations = face_recognition.face_locations(unknown_image)
			face_encodings = face_recognition.face_encodings(unknown_image,face_locations)

			for face in FaceData.objects.all():
				known_image = face_recognition.load_image_file(face.image_url)
				known_encoding = face_recognition.face_encodings(known_image)[0]
				for (top, right, bottom, left),face_encoding in zip(face_locations,face_encodings):
					results = face_recognition.compare_faces([known_encoding],face_encoding)
					if results[0] == True:
						text_width, text_height = img_draw.textsize(face.name)
						img_draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
						img_draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
						img_draw.text((left + 6, bottom - 5), face.name, (255,255,255,255), font=None, anchor=None)

			del img_draw
			img.save("image_with_boxes.jpg")
			img.show()
			#design train successfull page
			return render(request, 'recognizer/face_results.html', {'image_url': image_url})
