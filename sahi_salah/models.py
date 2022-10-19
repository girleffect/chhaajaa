from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from sahi_salah.block import TestimonialList, FAQCardList


class SahiSalahIndexPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )

    body = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])

    section_1 = models.CharField(max_length=250,blank=True, null=True)

    
    card_1_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    card_1 = models.CharField(max_length=200, help_text="intro of the section")
    card_2_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    card_2 = models.CharField(max_length=200, help_text="intro of the section")
    card_3_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    card_3 = models.CharField(max_length=200, help_text="intro of the section")
    content = StreamField(
        [
            ("faqcard", FAQCardList()),      
            ("testimonial", TestimonialList()),      
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body'),
        FieldPanel('section_1'),
        ImageChooserPanel('card_1_image'),
        FieldPanel('card_1'),
        ImageChooserPanel('card_2_image'),
        FieldPanel('card_2'),
        ImageChooserPanel('card_3_image'),
        FieldPanel('card_3'),        
        StreamFieldPanel("content"),
    ]


class SahiSalahPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )


    event_title = models.CharField(max_length=250,blank=True, null=True)

    
    event_body = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    
    instruction_title = models.CharField(max_length=250,blank=True, null=True)
    
    instruction_body = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])


    timing_title = models.CharField(max_length=250,blank=True, null=True)
    timing_date = models.DateField(max_length=250,blank=True, null=True)
    timing_time = models.TimeField(max_length=250,blank=True, null=True)
    price_title = models.CharField(max_length=250,blank=True, null=True)
    price_body = models.CharField(max_length=250,blank=True, null=True)
    location_title = models.CharField(max_length=250,blank=True, null=True)
    location_body = models.CharField(max_length=250,blank=True, null=True)

    whatsapp_text = models.CharField(max_length=200, help_text="intro of the section")
    whatsapp_link = models.CharField(max_length=200, help_text="intro of the section")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['events'] = SahiSalahPage.objects.all().exclude(id=self.id)
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('event_title'),
        FieldPanel('event_body'),
        FieldPanel('instruction_title'),
        FieldPanel('instruction_body'),
        FieldPanel('timing_title'),
        FieldPanel('timing_date'),
        FieldPanel('timing_time'),
        FieldPanel('price_title'),
        FieldPanel('price_body'),
        FieldPanel('location_title'),
        FieldPanel('location_body'),
        FieldPanel('whatsapp_text'),
        FieldPanel('whatsapp_link'),
    ]
