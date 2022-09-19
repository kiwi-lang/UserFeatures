from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("login/<int:project_id>", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("register/<int:project_id>", views.register, name="register"),

    path("logout", views.logout_view, name="logout"),
    path("logout/<int:project_id>", views.logout_view, name="logout"),

    path("profile", views.profile, name="profile"),

    path("projects", views.project_find, name="project_find"),
    path("project/new", views.project_new, name="project_new"),
    path("project/<int:project_id>/delete", views.project_delete, name="project_delete"),
    path("project/<int:project_id>", views.project_show, name="project_show"),
    path("project/<int:project_id>/page/<int:page>", views.project_show, name="project_show"),

    path("project/<int:project_id>/top/page/<int:page>", views.project_show_top, name="project_show_top"),
    path("project/<int:project_id>/rising/page/<int:page>", views.project_show_rising, name="project_show_rising"),
    path("project/<int:project_id>/latest/page/<int:page>", views.project_show_latest, name="project_show_latest"),
    path("project/<int:project_id>/tag/<int:tag_id>/page/<int:page>", views.project_show_tags, name="project_show_tag"),

    path("project/<int:project_id>/tag/new", views.tag_new, name="tag_new"),
    path("project/<int:project_id>/tag/<int:tag_id>/delete", views.tag_delete, name="tag_delete"),

    path("project/<int:project_id>/feature/find", views.feature_find, name="feature_find"),
    path("project/<int:project_id>/feature/new", views.feature_new, name="feature_new"),
    path("project/<int:project_id>/feature/<int:feature_id>/delete", views.feature_delete, name="feature_delete"),
    path("project/<int:project_id>/feature/<int:feature_id>", views.feature_show, name="feature_show"),
    path("project/<int:project_id>/feature/<int:feature_id>/comment", views.feature_comment, name="feature_comment"),
    path("project/<int:project_id>/feature/<int:feature_id>/tag/add", views.feature_tag_add, name="feature_tag_add"),
    path("project/<int:project_id>/feature/<int:feature_id>/tag/remove/<int:tag_id>", views.feature_tag_remove, name="feature_tag_remove"),

    path("project/<int:project_id>/feature/<int:feature_id>/up", views.feature_upvote, name="feature_upvote"),
    path("project/<int:project_id>/feature/<int:feature_id>/down", views.feature_downvote, name="feature_downvote"),

    path("project/<int:project_id>/feature/<int:feature_id>/up/main", views.feature_upvote_project, name="feature_upvote_project"),
    path("project/<int:project_id>/feature/<int:feature_id>/down/main", views.feature_downvote_project, name="feature_downvote_project"),
]
