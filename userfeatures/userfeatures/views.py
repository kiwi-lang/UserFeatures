import math
import datetime

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, F



from .models import User, Project, Feature, ProjectTags, Comment, Votes


def index(request):
    return render(
        request, "userfeatures/index.html", {"listings": []}
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "userfeatures/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "userfeatures/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "userfeatures/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "userfeatures/login_register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "userfeatures/login_register.html")


@login_required
def profile(request):
    projects = Project.objects.filter(owner=request.user)[:50]

    return render(
        request,
        "userfeatures/profile.html",
        dict(
            projects=projects,
        ),
    )

@login_required
def project_new(request):

    if request.method == "POST":
        # Create a new project
        project = Project.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            owner=request.user,
            banner=request.POST["image"],
        )
        project.save()

        # redirect to the project page
        return redirect(project_show, project.id)

    # show the form
    return render(
        request,
        "userfeatures/project_new.html",
    )


def project_find(request):
    pass


def project_show_top(request, project_id, page=0):
    return project_show(request, project_id, page, mode="top")


def project_show_rising(request, project_id, page=0):
    return project_show(request, project_id, page, mode="rising")


def project_show_latest(request, project_id, page=0):
    return project_show(request, project_id, page, mode="latest")


def project_show_tags(request, project_id, tag_id, page=0):
    return project_show(request, project_id, page, mode="top", tags=(tag_id,))

def project_show(request, project_id, page=0, mode="top", tags=None, all=False):
    step = 50

    project = Project.objects.get(id=project_id)

    if tags is not None:
        features = Feature.objects.filter(project=project_id, tags__in=tags)

    elif mode == "top":
        features = Feature.objects.filter(project=project_id).order_by("-votes")

    elif mode == 'latest':
        features = Feature.objects.filter(project=project_id).order_by("-created_datetime")

    elif mode == 'rising':
        features = Feature.objects.filter(project=project_id).order_by("-updated_datetime")

    else:
        features = Feature.objects.filter(project=project_id)

    tags = ProjectTags.objects.filter(project=project_id)
    feature_count = len(Feature.objects.filter(project=project_id))
    page_count = math.ceil(feature_count / step)

    if not all:
        features = features[step * page:step * (page + 1)]

    return render(
        request,
        "userfeatures/project.html",
        dict(
            project_id=project_id,
            project=project,
            features=features,
            tags=tags,
            feature_count=feature_count,
            pages=range(page_count) if page_count > 1 else [],
        )
    )


def feature_find(request, project_hint):
    # from django.contrib.postgres.search import SearchVector

    # Feature.objects.annotate(
    #     search=SearchVector('name', 'description'),
    # ).filter(search)

    options = Feature.objects.filter(title__search=project_hint)

    return JsonResponse(options)

@login_required
def feature_new(request, project_id):

    if request.method == "POST":
        # Every user can create new features
        feature = Feature.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project=Project.objects.get(id=project_id),
            owner=request.user,
            upvotes=1,
            downvotes=0
        )
        feature.save()

        # redirect to the feature page
        return redirect(feature_show, project_id, feature.id)

    project = Project.objects.get(id=project_id)

    return render(
        request,
        "userfeatures/feature_new.html",
        dict(project_id=project_id, project=project)
    )

@login_required
def feature_tag(request, project_id, feature_id):
    """Add a tag to a given feature"""

    if request.method == "POST":
        project = Project.objects.get(id=project_id)

        # Only the project owner can create tags
        if project.owner == request.user:
            tag_ids = request.POST["tag"]
            feature = Feature.objects.get(id=feature_id)
            for tag_id in tag_ids:
                feature.tags.add(tag_id)
            feature.save()

    return redirect(feature_show, project_id, feature_id)


@login_required
def feature_show(request, project_id, feature_id):
    if request.method == "POST":
        comment = Comment.objects.create(
            owner=request.user,
            feature=Feature.objects.get(id=feature_id),
            text=request.POST["content"],
        )
        comment.save()

    project = Project.objects.get(id=project_id)
    feature = Feature.objects.get(id=feature_id)
    comments = Comment.objects.filter(feature_id=feature_id)
    tags = ProjectTags.objects.filter(project=project)

    return render(
        request,
        "userfeatures/feature.html",
        dict(
            project=project,
            project_id=project_id,
            feature_id=feature_id,
            feature=feature,
            comments=comments,
            total=feature.upvotes - feature.downvotes,
            tags=tags,
        )
    )




def add_vote(request, project_id, feature_id, vote_value):
    old_vote = 0
    feature = Feature.objects.get(id=feature_id)

    try:
        vote = Votes.objects.get(
            owner=request.user,
            feature=feature,
        )
        old_vote = vote.vote
        vote.vote = vote_value

    except Votes.DoesNotExist:
        vote = Votes.objects.create(
            owner=request.user,
            feature=feature,
            vote=vote_value,
        )

    vote.save()
    return old_vote


def user_vote(request, project_id, feature_id, vote_value):
    """The accounting does not need to be perfect all the time.
    To lessen the computation impact we could just to a update_or_create a vote,
    and have a background task update the counts periodically.
    """
    old_vote = add_vote(request, project_id, feature_id, vote_value)

    # we are voting the same so ignore
    if old_vote == vote_value:
        return

    # this is a new vote
    if old_vote == 0:
        if vote_value > 0:
            Feature.objects.filter(id=feature_id).update(upvotes=F('upvotes') + 1, updated_datetime=datetime.datetime.now())
        else:
            Feature.objects.filter(id=feature_id).update(downvotes=F('downvotes') + 1, updated_datetime=datetime.datetime.now())

    else:
        # We changed our vote
        if vote_value > 0:
            Feature.objects.filter(id=feature_id).update(
                upvotes=F('upvotes') + 1, downvotes=F('downvotes') - 1, updated_datetime=datetime.datetime.now()
            )
        else:
            Feature.objects.filter(id=feature_id).update(
                upvotes=F('upvotes') - 1, downvotes=F('downvotes') + 1, updated_datetime=datetime.datetime.now()
            )


@login_required
def feature_downvote_project(request, project_id, feature_id):
    return feature_downvote(request, project_id, feature_id, False)


@login_required
def feature_upvote_project(request, project_id, feature_id):
    return feature_upvote(request, project_id, feature_id, False)


@login_required
def feature_upvote(request, project_id, feature_id, feature=True):

    user_vote(request, project_id, feature_id, 1)

    if feature:
        return redirect(feature_show, project_id, feature_id)

    return redirect(project_show, project_id)


@login_required
def feature_downvote(request, project_id, feature_id, feature=True):
    user_vote(request, project_id, feature_id, -1)

    if feature:
        return redirect(feature_show, project_id, feature_id)

    return redirect(project_show, project_id)


@login_required
def tag_new(request, project_id):
    project = Project.objects.get(id=project_id)
    tags = ProjectTags.objects.filter(project=project_id)

    if request.method == "POST":
        if project.owner == request.user:
            tag = ProjectTags.objects.create(
                tag=request.POST["name"],
                project=project,
            )
            tag.save()

    return render(
        request,
        "userfeatures/tag_new.html",
        dict(project_id=project_id, project=project, tags=tags)
    )
