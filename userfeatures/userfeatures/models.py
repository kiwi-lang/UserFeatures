from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Project(models.Model):
    """A project for which user can submit new feature request"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=50)
    description = models.TextField()
    banner = models.ImageField(upload_to="project_banners/", blank=True)


class Feature(models.Model):
    """A feature request that was submitted by a user"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=50)
    description = models.TextField()

    upvotes = models.IntegerField(default=1)
    downvotes = models.IntegerField(default=0)


class Comment(models.Model):
    """A comment on a feature request"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, default="")
    text = models.TextField()


class ProjectTags(models.Model):
    """Tag used by a project for its features"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    tag = models.CharField(max_length=50)


class FeatureTags(models.Model):
    """Tags for a feature request"""
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, default="")
    tag = models.ForeignKey(ProjectTags, on_delete=models.CASCADE, default="")


class Watchlist(models.Model):
    """A project watchlist of a given user"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
