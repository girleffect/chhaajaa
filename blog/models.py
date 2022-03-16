from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    button = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('intro'  ),
        ImageChooserPanel('image'),
        PageChooserPanel('button')
    ]

    def filter_blog(self, request):

        if request.GET.get('tag', None):
            tags = request.GET.getlist('tag')
            queryset = BlogPage.objects.filter(tags__slug__in=tags).child_of(self).live().distinct()
        else:
            queryset = BlogPage.objects.child_of(self).live().order_by("-date")
        return queryset


    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')

        # Update template context
        context = super().get_context(request)
        context['tags'] = BlogPage.tags.all()
        context["tags_name"] = request.GET.getlist('tag')
        context['blogpages'] = self.filter_blog(request)
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    # intro = models.CharField(max_length=250)
    body = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link','ul', 'ol', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ]
        )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['articles'] = BlogPage.objects.filter(tags__in=self.tags.all()).distinct().order_by('-date').exclude(id=self.id)
        return context

    search_fields = Page.search_fields + [
        # index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        # FieldPanel('intro'),
        FieldPanel('tags'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]