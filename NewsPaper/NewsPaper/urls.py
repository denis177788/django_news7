from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
 # path('', include('protect.urls')),
   path('profile/', include('protect.urls')),
   path('', lambda request: redirect('news/', permanent=False)),
   path('sign/', include('sign.urls')),
 # path('accounts/', include('allauth.urls')),   # временно отключил модуль allauth
 # path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('articles/', include('news.urls1')),
]