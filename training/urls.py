from django.urls import path

from . import views

urlpatterns = [
    path("", views.train, name="train"),
    path("abort/", views.abort, name="abort"),
    path("last_data/", views.get_last_train_data, name="last_data"),
    path("process/<str:p_id>/", views.get_process_data, name="process"),
]