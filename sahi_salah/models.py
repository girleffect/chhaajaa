from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from django.utils.timezone import now
from sahi_salah.block import Testimonial, FAQCardList, CrousalHeader
from home.block import FAQCard


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
    whatsapp_link = models.CharField(max_length=200, help_text="intro of the section")
    faqs = StreamField(
        [
            ("faqcard", FAQCard()),
        ],
        null=True,
        blank=True,
    )
    
    testimonials = StreamField(
        [
            ("testimonials", Testimonial()),
        ],
        null=True,
        blank=True,
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['upcoming_event'] = UpcomingEventsArticle.objects.live().filter(timing_date__gt=now()).exclude(id=self.id)
        context['past_event'] = UpcomingEventsArticle.objects.live().filter(timing_date__lt=now()).exclude(id=self.id)
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body'),
        FieldPanel('section_1'),
        FieldPanel('whatsapp_link'),
        ImageChooserPanel('card_1_image'),
        FieldPanel('card_1'),
        ImageChooserPanel('card_2_image'),
        FieldPanel('card_2'),
        ImageChooserPanel('card_3_image'),
        FieldPanel('card_3'),        
        StreamFieldPanel("faqs"),
        StreamFieldPanel('testimonials')
    ]


class UpcomingEventsArticle(Page):
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
    cta_button = models.CharField(max_length=200, help_text="intro of the section")
    content = StreamField(
        [
            ('crousalheader',CrousalHeader()),   
        ],
        null=True,
        blank=True,
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['events'] = UpcomingEventsArticle.objects.all().exclude(id=self.id)
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
        FieldPanel('cta_button'),
        StreamFieldPanel("content"),
    ]
