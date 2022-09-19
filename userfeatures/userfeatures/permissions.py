from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


from .models import Project, Feature, ProjectTags, Comment, Votes, User

meta_user, _ = User.objects.get_or_create(id=0)
meta_user.set_unusable_password()


meta_project, _ = Project.objects.get_or_create(
    id=0,
    owner=meta_user,
    name="Userfeatures",
    description="Userfeature is a website for community driven development",
)

project_type = ContentType.objects.get_for_model(Project)
can_create_project, _ = Permission.objects.get_or_create(
    codename="can_create_projects",
    name="Can create new projects",
    content_type=project_type,
)


comment_type = ContentType.objects.get_for_model(Comment)
can_comment, _ = Permission.objects.get_or_create(
    codename="can_comment",
    name="Can write comments",
    content_type=comment_type,
)


feature_type = ContentType.objects.get_for_model(Feature)
can_create_features, _ = Permission.objects.get_or_create(
    codename="can_create_features",
    name="Can create features",
    content_type=feature_type,
)


vote_type = ContentType.objects.get_for_model(Votes)
can_vote, _ = Permission.objects.get_or_create(
    codename="can_vote",
    name="Can vote on features",
    content_type=vote_type,
)

tag_type = ContentType.objects.get_for_model(ProjectTags)
can_create_tag, _ = Permission.objects.get_or_create(
    codename="can_create_tags",
    name="Can create new tags",
    content_type=tag_type,
)


voter_group, created = Group.objects.get_or_create(name="voter")
voter_group.permissions.set(
    [
        can_vote,
        can_comment,
        can_create_features,
    ]
)

project_onwer, created = Group.objects.get_or_create(name="project_onwer")
project_onwer.permissions.set(
    [
        can_vote,
        can_comment,
        can_create_features,
        # ---
        can_create_tag,
        can_create_project,
    ]
)
