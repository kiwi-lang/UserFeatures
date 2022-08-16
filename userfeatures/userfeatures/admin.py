from django.contrib import admin
from .models import User, Project, Feature, ProjectTags, Comment, FeatureTags, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Feature)
admin.site.register(Comment)
admin.site.register(ProjectTags)
admin.site.register(FeatureTags)
admin.site.register(Watchlist)
