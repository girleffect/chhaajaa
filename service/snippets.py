from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from django.utils.text import slugify
from django.db import models


class ConcernTag(TaggedItemBase):
    content_object = models.ForeignKey(
        'ConcernPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


@register_snippet
class ConcernPage(models.Model):
    """
    This page used as child of service index page.
    """
    intro = models.CharField(max_length=250)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    tags = TaggableManager(through=ConcernTag)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True
    )
    panels = [
        FieldPanel('intro'),
        FieldPanel("tags"),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name_plural = 'Concerns'

    def __str__(self):
        return self.intro

    def _get_unique_slug(self):
        slug = slugify(self.intro)
        unique_slug = slug
        num = 1
        if self.intro:
            while ConcernPage.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


@register_snippet
class ServiceLocation(models.Model):
    """
    This class is used for save location
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while ServiceLocation.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


@register_snippet
class ServiceCategory(models.Model):
    """
    This class is used for service category.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while ServiceCategory.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


@register_snippet
class SocialPage(models.Model):
    """
    This class is used for social site which are shown in homepage.
    """

    name = models.CharField(max_length=100, help_text="Name of the social site.", null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True
    )
    website_link = models.URLField(max_length=500, help_text="Url of the social page.")
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('website_link'),

    ]

    class Meta:
        verbose_name_plural = 'Socials'

    def __str__(self):
        return self.name

@register_snippet
class VideoSection(models.Model):
    """
    This class is used for video and images which are shown in homepage.
    """

    name = models.CharField(max_length=100, help_text="Name of the video")
    description = models.TextField()
    video_link = models.URLField(max_length=500, help_text="Url of the video", null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True,
        help_text="if you are adding image then Please add image link also and don't add video link")

    image_link = models.URLField(max_length=500, help_text="Url of the social page.", null=True, blank=True)
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('video_link'),
        ImageChooserPanel('image'),
        FieldPanel('image_link'),

    ]
    class Meta:
        verbose_name_plural = 'Arrey Dekho'

    def __str__(self):
        return self.name
