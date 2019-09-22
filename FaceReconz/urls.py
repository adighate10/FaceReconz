from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from recognizer import views as recognizer_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recognizer/', include('recognizer.urls')),
    url(r'^$',recognizer_views.index , name="home"),
    url(r'^crosssite/$',recognizer_views.crosssite , name="xss"),
    url(r'^accounts/', include('accounts.urls')),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
