from django.urls import path
from obsfeare_server.app.views import trees_views

app_name = "app"

urlpatterns = [
    path("", trees_views.index, name="get-trees"),
    path("gpt/new", trees_views.create_tree, name="create-tree"),
    path(
        "gpt/append/<str:tree_id>/<str:node_id>",
        trees_views.append_node,
        name="append-node",
    ),
]
