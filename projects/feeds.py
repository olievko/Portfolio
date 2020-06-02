from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Project


class LatestProjectsFeed(Feed):
    title = 'My project'
    link = '/project/'
    description = 'New illustrations of my portfolio.'

    def items(self):
        return Project.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.description, 30)
