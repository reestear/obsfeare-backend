from django.urls import path
from obsfeare_server.app.views import history_views

app_name = "app"

urlpatterns = [
    path("", history_views.index, name="history-list"),
]
