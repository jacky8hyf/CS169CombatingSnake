"""combatingSnake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from gameStart import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.homePage),
    # TODO: REFACTOR FILES IN NEXT ITERATION TO USE STATIC SERVING INSTEAD
    #url(r'^$', serve, kwargs = {'path': 'templates/index.html', 'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users(/|)$', views.UsersView.as_view()),
    url(r'^users/login(/|)$', views.UsersLoginView.as_view()),
    url(r'^users/(?P<userId>\w*?)(/|)$', views.SingleUserView.as_view()),
    url(r'^rooms(/|)$', views.RoomsView.as_view()),
    url(r'^rooms/(?P<roomId>\w*?)(/|)$', views.SingleRoomView.as_view()),
    url(r'^rooms/(?P<roomId>\w*?)/members(/|)$',
    views.SingleRoomMembersView.as_view()),
    url(r'^rooms/(?P<roomId>\w*?)/members/(?P<memberId>\w*?)(/|)$',
        views.SingleRoomSingleMemberView.as_view()),
]
