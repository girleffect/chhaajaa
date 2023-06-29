from django.db import models
from home.block import FAQCard

# Create your models here.
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from bakBakGangIndex.block import BBG2TestimonialSection, BBGCardFooterSection, BBGCards1Section, BBGCards2Section, BBGTestimonialSection, BolbehanSection3Cards, BolbehanSection4Cards


class BakBakGangIndexPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )

    section_1 = models.CharField(max_length=250,blank=True, null=True)

    
    section_1_title_1 = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_1_card_01 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_02 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_03 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_04 = models.CharField(max_length=200, help_text="intro of the section")

    section_1_title_2 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_11 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_12 = models.CharField(max_length=200, help_text="intro of the section")
    section_1_card_13 = models.CharField(max_length=200, help_text="intro of the section")


    section_2 = models.CharField(max_length=250,blank=True, null=True)

    section_2_title_1 = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_2_card = StreamField(
        [
            ("testimonial", BBGTestimonialSection()),
        ],
        null=True,
        blank=True,
    )
    

    section_3 = models.CharField(max_length=250,blank=True, null=True)

    section_3_title_1 = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_3_card = StreamField(
        [
            ("cards", BBGCards1Section()),
        ],
        null=True,
        blank=True,
    )
    

    section_4 = models.CharField(max_length=250,blank=True, null=True)

    section_4_card = StreamField(
        [
            ("cards", BBGCards2Section()),
        ],
        null=True,
        blank=True,
    )


    section_5 = models.CharField(max_length=250,blank=True, null=True)

    
    section_5_title = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_5_card_01 = models.CharField(max_length=200, help_text="intro of the section")
    section_5_card_02 = models.CharField(max_length=200, help_text="intro of the section")
    section_5_card_03 = models.CharField(max_length=200, help_text="intro of the section")
    section_5_card_04 = models.CharField(max_length=200, help_text="intro of the section")

    section_5_banner = models.CharField(max_length=250,blank=True, null=True)


    section_footer_title = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_footer_subtitle = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_footer_banner = models.ForeignKey('wagtailimages.Image',
                                           on_delete=models.SET_NULL, related_name='+', null=True)


    faqcard = StreamField(
        [
            ("faqcard", FAQCard()),          
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('section_1'),
        FieldPanel('section_1_title_1'),
        FieldPanel('section_1_card_01'),
        FieldPanel('section_1_card_02'),
        FieldPanel('section_1_card_03'),
        FieldPanel('section_1_card_04'),
        FieldPanel('section_1_title_2'),
        FieldPanel('section_1_card_11'),
        FieldPanel('section_1_card_12'),
        FieldPanel('section_1_card_13'),
        FieldPanel('section_2'),
        FieldPanel('section_2_title_1'),
        StreamFieldPanel("section_2_card"),
        FieldPanel('section_3'),
        FieldPanel('section_3_title_1'),
        StreamFieldPanel("section_3_card"),
        FieldPanel('section_4'),
        StreamFieldPanel("section_4_card"),
        FieldPanel('section_5'),
        FieldPanel('section_5_title'),
        FieldPanel('section_5_card_01'),
        FieldPanel('section_5_card_02'),
        FieldPanel('section_5_card_03'),
        FieldPanel('section_5_card_04'),
        ImageChooserPanel('section_5_banner'),
        FieldPanel('section_footer_title', classname="full"),
        FieldPanel('section_footer_subtitle', classname="full"),
        ImageChooserPanel('section_footer_banner'),
        StreamFieldPanel("faqcard"),
    ]


class BolBehanPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    background_header_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    header_title = models.CharField(max_length=255,blank=True)
    header_subtitle = RichTextField(blank=True,features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    whatsapp_text = models.CharField(max_length=200, help_text="intro of the section")
    whatsapp_url = models.CharField(max_length=200,blank=True)
    whatsapp_icon = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    messenger_text = models.CharField(max_length=200,blank=True)
    messenger_url = models.CharField(max_length=200,blank=True)
    messenger_icon = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    section_1 = models.CharField(max_length=250,blank=True, null=True)

    
    section_1_title_1 = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])
    section_1_sub_title_1 = models.CharField(max_length=250,blank=True, null=True)    

    section_1_main_img_1 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )

    section_1_main_img_2 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )

    section_2 = models.CharField(max_length=250,blank=True, null=True)

    section_2_main_img_1 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    section_2_card = StreamField(
        [
            ("testimonial", BBG2TestimonialSection()),
        ],
        null=True,
        blank=True,
    )
    

    section_3_card = StreamField(
        [
            ("section_3_cards", BolbehanSection3Cards()),
        ],
        null=True,
        blank=True,
    )
    

    section_4 = models.CharField(max_length=250,blank=True, null=True)

    section_4_main_img_1 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )


    section_4_description = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])

    section_4_card = StreamField(
        [
            ("section_4_cards", BolbehanSection4Cards()),
        ],
        null=True,
        blank=True,
    )


    section_5 = models.CharField(max_length=250,blank=True, null=True)
    section_5_main_img_1 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    section_5_description = RichTextField(blank=True, features=[
        'h1','h2', 'h3','h4','h5','h6', 'bold', 'italic',
         'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed',
           'code', 'blockquote', 'superscript', 'subscript', 'strikethrough'
        ])


    section_footer = StreamField(
        [
            ("cards", BBGCardFooterSection()),
        ],
        null=True,
        blank=True,
    )    


    faqcard = StreamField(
        [
            ("faqcard", FAQCard()),          
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('header_title'),
        FieldPanel('header_subtitle'),
        ImageChooserPanel('background_header_image'),
        ImageChooserPanel('header_image'),
        FieldPanel('whatsapp_text'),
        FieldPanel('whatsapp_url'),
        ImageChooserPanel('whatsapp_icon'),
        FieldPanel('messenger_text'),
        FieldPanel('messenger_url'),
        ImageChooserPanel('messenger_icon'),
        FieldPanel('section_1'),
        FieldPanel('section_1_title_1'),
        FieldPanel('section_1_sub_title_1'),
        ImageChooserPanel('section_1_main_img_1'),
        ImageChooserPanel('section_1_main_img_2'),
        
        FieldPanel('section_2'),
        ImageChooserPanel('section_2_main_img_1'),
        StreamFieldPanel("section_2_card"),


        StreamFieldPanel("section_3_card"),

        FieldPanel('section_4'),
        ImageChooserPanel('section_4_main_img_1'),
        FieldPanel('section_4_description', classname="web-text"),
        StreamFieldPanel("section_4_card"),


        FieldPanel('section_5'),
        FieldPanel('section_5_description'),
        ImageChooserPanel('section_5_main_img_1'),

        StreamFieldPanel("section_footer"),
        StreamFieldPanel("faqcard"),
    ]
