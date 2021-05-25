from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from store import views as views_store


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('register', views_store.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='store/templates/login.html'), name='login-page'),
]
urlpatterns += [
  re_path(r'^static/(?:.*)$', serve, {'document_root': settings.STATIC_ROOT,})
]


