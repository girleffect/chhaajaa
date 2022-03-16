from django.contrib.syndication.views import Feed
from blog.models import BlogPage
from django.utils.feedgenerator import Atom1Feed


class RssFeed(Feed):
    title = "chhaajaa.com"
    link = "/"
    description = "Chhaa Jaa, jo har hafte aapke liye laayega dher saari knowledge! Humaare website par har wo sawal ka jawab paye jo aap poochne se darte hai."
    feed_url = '/rss/'
    author_name = 'chhaajaa.com'
    categories = ()
    feed_copyright = 'Copyright (c) 2019-2020, chhaajaa.com'
    description_template = 'feeds/beat_description.html'
    language = 'en'

    def items(self):
        return BlogPage.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    # return a short description of article
    def item_description(self, item):
        return item.body


    # return the URL of the article
    def item_link(self, item):
        return item.full_url

    # return the date the article was published
    def item_pubdate(self, item):
        return item.first_published_at

    # return the date of the last update of the article
    def item_updateddate(self, item):
        return item.last_published_at

    # return the categories of the article
    def item_tags(self, item):
        return item.tags.all()


class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    link = "/atom/"
    subtitle = RssFeed.description