# Create your models here.
from django.shortcuts import render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel

from blog.models import BlogPage
from service.snippets import ConcernPage, ServiceLocation, ServiceCategory
from django import forms

from .api.serializers import CategorySerlializer, ConcernSerlializer, LocationSerializer


class ConcernIndexPage(RoutablePageMixin, Page):
    """
    This page use as index page of concern.
    """

    intro = RichTextField(
        blank=True,
        features=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "document-link",
            "image",
            "embed",
            "code",
            "blockquote",
            "superscript",
            "subscript",
            "strikethrough",
        ],
    )
    custom_text = RichTextField(
        blank=True,
        features=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "document-link",
            "image",
            "embed",
            "code",
            "blockquote",
            "superscript",
            "subscript",
            "strikethrough",
        ],
    )
    description = RichTextField(
        blank=True,
        features=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "document-link",
            "image",
            "embed",
            "code",
            "blockquote",
            "superscript",
            "subscript",
            "strikethrough",
        ],
    )
    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("custom_text", classname="full"),
        FieldPanel("description", classname="full"),
    ]

    def get_concern(self, request):

        if request.GET.get("tag", None):
            tags = request.GET.getlist("tag")
            queryset = ConcernPage.objects.filter(tags__slug__in=tags).distinct()
        else:
            queryset = ConcernPage.objects.all()
        return queryset

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        concerns = self.get_concern(request)
        context["services"] = concerns
        context["categories"] = ServiceCategory.objects.all()
        return context

    def get_services(self, request, *args, **kwargs):

        filters = {}

        if request.GET.get("location"):
            filters["location__slug"] = request.GET.get("location")

        if request.GET.get("service"):
            filters["concern__slug"] = request.GET.get("service")
        if request.GET.get("tag", None):
            tags = request.GET.getlist("tag")
            filters["tags__slug__in"] = tags

        return ServicePage.objects.filter(**filters).distinct().live()

    def related_article(self, request, *args, **kwargs):

        tags = request.GET.getlist('tag')
        queryset = BlogPage.objects.filter(tags__slug__in=tags).live()

        return queryset

    @route(r'^services/$')
    def filter_services(self, request, *args, **kwargs):
        """
        This is the routable page is used for show the service according to concern.
        """
        context = self.get_context(request, *args, **kwargs)
        context['service_list'] = self.get_services(request)
        context['concerns'] = ConcernPage.objects.all()
        context['locations'] = ServiceLocation.objects.all()
        context['tags'] = ServicePage.tags.all()
        context["tags_name"] = request.GET.getlist('tag')
        context['articles'] = self.related_article(request)
        return render(request, "service/filter_list.html", context)


class ServicePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "ServicePage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class ServicePage(Page):
    """
    This page use as service page
    """

    name = models.CharField(max_length=250)
    caption = models.CharField(max_length=250, blank=True, null=True)
    description = RichTextField(
        blank=True,
        features=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "document-link",
            "image",
            "embed",
            "code",
            "blockquote",
            "superscript",
            "subscript",
            "strikethrough",
        ],
    )
    timing = models.CharField(max_length=255, help_text="e.g. 9am-12pm")
    price = models.CharField(max_length=255)
    external_link = models.CharField(
        max_length=500, help_text="Add a external link or contact of website."
    )
    concern = ParentalManyToManyField(
        "ConcernPage",
        blank=True,
    )
    location = ParentalManyToManyField(
        "ServiceLocation",
        blank=True,
    )
    category = models.ForeignKey(
        "ServiceCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    tags = ClusterTaggableManager(through=ServicePageTag, blank=True)

    # API fields for the service API.
    api_fields = [
        APIField("name"),
        APIField("description"),
        APIField("timing"),
        APIField("price"),
        APIField("external_link"),
        APIField("concern", serializer=ConcernSerlializer()),
        APIField("location", serializer=LocationSerializer()),
        APIField("category", serializer=CategorySerlializer()),
        APIField("tags"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("caption"),
        FieldPanel("concern", widget=forms.CheckboxSelectMultiple),
        FieldPanel("location", widget=forms.CheckboxSelectMultiple),
        FieldPanel("category"),
        FieldPanel("tags"),
        FieldPanel("timing"),
        FieldPanel("price"),
        FieldPanel("external_link"),
        FieldPanel("description", classname="full"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        tags = [tag.slug for tag in self.tags.all()]
        context['articles'] = BlogPage.objects.filter(tags__slug__in=tags).live()
        context['services'] = ServicePage.objects.filter(tags__slug__in=tags).exclude(id=self.id).live()
        return context


class ServicePageGalleryImage(Orderable):
    """
    This page is used as gallery for service page.
    """

    page = ParentalKey(
        ServicePage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
    ]
