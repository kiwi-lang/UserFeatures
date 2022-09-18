from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models



class User(AbstractUser):
    pass


class Setting(models.Model):
    """Userfeatures settings"""
    name = models.IntegerField(unique=True, primary_key=True)
    value = models.IntegerField(default=0)


class Project(models.Model):
    """A project for which user can submit new feature request"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=50)
    description = models.TextField()
    banner = models.ImageField(upload_to="project_banners/", blank=True)

    created_datetime = models.DateTimeField(auto_now_add=True)


class ProjectTags(models.Model):
    """Tag used by a project for its features"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    tag = models.CharField(max_length=50)
    style = models.CharField(max_length=50, blank=True)


class Feature(models.Model):
    """A feature request that was submitted by a user"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=50)
    description = models.TextField()

    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    anon_upvotes = models.IntegerField(default=1)
    anon_downvotes = models.IntegerField(default=0)

    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(ProjectTags)

    @property
    def votes(self):
        return self.upvotes - self.downvotes


class Votes(models.Model):
    """Table to record user votes on features, to prevent user from voting twice"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, default="")
    vote = models.IntegerField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'feature'], name='unique_votes')
        ]


class Comment(models.Model):
    """A comment on a feature request"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, default="")
    text = models.TextField()

    created_datetime = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    """A project watchlist of a given user"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)




project_type = ContentType.objects.get_for_model(Project)
can_create_project = Permission.objects.create(
    codename='can_create_projects',
    name='Can create new projects',
    content_type=project_type,
)


comment_type = ContentType.objects.get_for_model(Comment)
can_comment = Permission.objects.create(
    codename='can_comment',
    name='Can write comments',
    content_type=comment_type,
)


feature_type = ContentType.objects.get_for_model(Feature)
can_create_features = Permission.objects.create(
    codename='can_create_features',
    name='Can create features',
    content_type=feature_type,
)


vote_type = ContentType.objects.get_for_model(Votes)
can_vote = Permission.objects.create(
    codename='can_vote',
    name='Can vote on features',
    content_type=vote_type,
)

tag_type = ContentType.objects.get_for_model(ProjectTags)
can_create_tag = Permission.objects.create(
    codename='can_create_tags',
    name='Can create new tags',
    content_type=tag_type,
)


voter_group, created = Group.objects.get_or_create(name='voter')

if created:
    voter_group.permissions.add(
        'userfeatures.can_vote',
        'userfeatures.can_comment',
        'userfeatures.can_create_features',
    )


project_onwer, created = Group.objects.get_or_create(name='project_onwer')

if created:
    project_onwer.permissions.add(
        'userfeatures.can_vote',
        'userfeatures.can_comment',
        'userfeatures.can_create_features',
        'userfeatures.can_create_tags',
        'userfeatures.can_create_projects',
    )
