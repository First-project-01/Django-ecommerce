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
    path('password-reset',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
urlpatterns += [
    re_path(r'^static/(?:.*)$', serve, {'document_root': settings.STATIC_ROOT, })
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
