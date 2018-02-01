"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
import main.views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main.views.index),
    path('register/',main.views.index),
    path('login/',main.views.sign_in),
    path('logout/',main.views.sign_out),
    path('post/',main.views.post),
    path('user/<str:username>/',main.views.user_profile),
    path('hashtag/<str:text>/',main.views.hashtag),
    path('posts/<int:pid>/',main.views.posts),
    path('api/',main.views.api),
    path('upload/',main.views.upload),
    path('add-member/<int:cid>/',main.views.add_member),
    path('remove-member/<int:cid>/',main.views.remove_member),
    path('create-chat/',main.views.create_chat),
    path('send-message/<int:cid>/',main.views.send_message),
    path('get-messages/<int:cid>/',main.views.get_messages),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
