from django.urls import path

from . import views
from stream.views import get_stream
urlpatterns = [
    path("stream/<str:node_id>/", get_stream, name="stream"),
]