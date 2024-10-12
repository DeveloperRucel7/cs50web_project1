from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("search", views.search, name="search"),
    path("add-page", views.add_page, name="add_page"),
    path("edit-page", views.edit_page, name="edit_page"),
    path("save-page", views.save_page, name="save_page"),
    path("random-page", views.random_page, name="random_page"),
]
