from django.conf.urls import url
from . import views

app_name = 'recognizer'

urlpatterns = [
	url(r'^$',views.index, name = "index"),
	url(r'^train/$', views.train_model, name="train"),
	url(r'^reveal/$', views.reveal_faces, name="reveal"),
	url(r'^revealresult/$', views.reveal_results, name="reveal_results"),
]
