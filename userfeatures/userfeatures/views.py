from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, F

from .models import User, Project, Feature, ProjectTags, Comment, FeatureTags, Watchlist


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


def project_show(request, project_id):
    project = Project.objects.get(id=project_id)
    features = Feature.objects.filter(project=project_id)[:50]

    return render(
        request,
        "userfeatures/project.html",
        dict(
            project_id=project_id,
            project=project,
            features=features,
        )
    )


@login_required
def feature_new(request, project_id):
    if request.method == "POST":
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
def feature_show(request, project_id, feature_id):
    if request.method == "POST":
        # Add Comment
        pass

    project = Project.objects.get(id=project_id)
    feature = Feature.objects.get(id=feature_id)
    comments = Comment.objects.filter(feature_id=feature_id)

    return render(
        request,
        "userfeatures/feature.html",
        dict(
            project=project,
            project_id=project_id,
            feature_id=feature_id,
            feature=feature,
            comments=comments,
            total=feature.upvotes - feature.downvotes
        )
    )


@login_required
def feature_upvote(request, project_id, feature_id):
    Feature.objects.filter(id=feature_id).update(upvotes=F('upvotes') + 1)
    return redirect(feature_show, project_id, feature_id)


@login_required
def feature_downvote(request, project_id, feature_id):
    Feature.objects.filter(id=feature_id).update(downvotes=F('downvotes') + 1)
    return redirect(feature_show, project_id, feature_id)


# Display current user's watchlist
@login_required
def watchlist(request):

    if request.method == "POST":
        id = request.POST.get("listing_id")
        listing = AuctionListing.objects.get(id=id)
        if "remove" in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return HttpResponseRedirect(reverse("listing", args=[id, listing.title]))
        else:
            add_watchlist = Watchlist.objects.create(user=request.user, listing=listing)
            add_watchlist.save()

    users_watchlist: Watchlist = Watchlist.objects.filter(user=request.user)
    listings = list()
    for listing in users_watchlist:
        listings.append(getattr(listing, "listing"))
    return render(
        request,
        "userfeatures/watchlist.html",
        {"listings": listings},
    )


# Place for creating new lisitng (only for logged in user)
# @login_required
# def feature_new(request):
#     if request.method == "POST":
#         title = request.POST["title"]
#         description = request.POST["description"]
#         start_bid = request.POST["start_bid"]
#         image_url = request.POST["image"]
#         category = request.POST.get("category")
#         current_user = request.user
#         l = AuctionListing.objects.create(
#             title=title,
#             description=description,
#             start_bid=start_bid,
#             image=image_url,
#             category=category,
#             creator=current_user,
#         )
#         l.save()
#         return redirect(listing, l.id, l.title)
#     else:
#         return render(
#             request,
#             "userfeatures/feature_new.html",
#             {"categories": Category.objects.all()},
#         )


# List all categories, clicking on category name
# redirects user to list of active listings in that category
def categories(request):
    return render(
        request,
        "userfeatures/categories.html",
        {
            "categories": Category.objects.all(),
            "no_category": AuctionListing.objects.filter(category__isnull=True).count(),
        },
    )


def category(request, category):
    # If no category, filters all lisings with null category and lists all listings without Category
    if category == "Other":
        return render(
            request,
            "userfeatures/category_page.html",
            {
                "listings": AuctionListing.objects.filter(category__isnull=True),
                "category": category,
            },
        )
    else:
        category_id = Category.objects.get(category=category).id
        return render(
            request,
            "userfeatures/category_page.html",
            {
                "listings": AuctionListing.objects.filter(category=category_id),
                "category": category,
            },
        )


def listing(request, id, title):
    if request.method == "POST":
        listing = AuctionListing.objects.get(id=id)
        if "close" in request.POST:
            listing.active = False
            listing.save()
            # bids = Bid.objects.filter(listing=listing)
            # highest = bids.aggregate(Max("amount"))
            # if highest is None:
            #   listing.winner = None
            # else:
            #    listing.winner = getattr(
            #        Bid.objects.get(listing=listing, amount=highest), "bidder"
            #    )
        else:
            commenter = request.user
            content = request.POST.get("content")

            comment = Comment.objects.create(
                content=content, commenter=commenter, listing=listing
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    return render(
        request,
        "userfeatures/listing.html",
        {
            "listing": AuctionListing.objects.get(id=id),
            "comments": Comment.objects.filter(listing=id),
            "in_watchlist": Watchlist.objects.filter(
                listing=id, user=request.user
            ).count(),
            "winner": getattr(AuctionListing.objects.get(id=id), "winner"),
        },
    )
