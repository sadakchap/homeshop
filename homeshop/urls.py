from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from accounts.views import login_view, logout_view, register, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('register/',register, name='register'),
    path('', home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
