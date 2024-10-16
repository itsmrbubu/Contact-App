from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name ='index'),
    path("register", register, name='register'),
    path("login", login, name='login'),
    path("logout", logout, name='logout'),
    path("profile", profile, name='profile'),
    path("editProfile", editProfile, name = 'editProfile'),
    path("addContact", addContact, name = 'addContact'),
    path("contacts", showContacts, name = 'contacts'),
    path("showContact/<int:id>", showContact, name = 'showContact'),
    path("deleteContact/<int:id>", deleteContact, name = 'deleteContact'),
    path("editContact /<int:id>", editContact, name ='editContact'),
    path("search", search, name ='search'),
    path("export", export, name ='export'),
    path("send/<int:id>", send_message, name ='send'),
]
