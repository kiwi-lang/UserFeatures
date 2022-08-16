from unicodedata import category
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),

    path("projects", views.project_find, name="project_find"),
    path("project/new", views.project_new, name="project_new"),
    path("project/<int:project_id>", views.project_show, name="project_show"),
    path("project/<int:project_id>/feature/new", views.feature_new, name="feature_new"),
    path("project/<int:project_id>/feature/<int:feature_id>", views.feature_show, name="feature_show"),
    path("project/<int:project_id>/feature/<int:feature_id>/up", views.feature_upvote, name="feature_upvote"),
    path("project/<int:project_id>/feature/<int:feature_id>/down", views.feature_downvote, name="feature_downvote"),




    # path("categories", views.categories, name="categories"),
    # path("listing/<str:id>/<str:title>", views.listing, name="listing"),
    # path("categories", views.categories, name="categories"),
    # path("category/<str:category>", views.category, name="category"),
    # path("watchlist", views.watchlist, name="watchlist"),
]
