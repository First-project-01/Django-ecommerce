from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from store import views as views_store


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('register', views_store.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login-page'),
    url(r'^logout$', LogoutView.as_view(), name='logout-page'),
]
urlpatterns += [
  re_path(r'^static/(?:.*)$', serve, {'document_root': settings.STATIC_ROOT,})
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
