from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class Testimonial(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Enter title")
    
    class Meta:
        template = "block/testimonials.html"
        icon = "edit"
        label = "Testimonial List"


class TestimonialList(blocks.StructBlock):
    testimonial = blocks.ListBlock(Testimonial())
    
    class Meta:
        template = "block/testimonials.html"
        icon = "edit"
        label = "Testimonial List"


class FAQCard(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Enter title")
    description = blocks.RichTextBlock(required=False, help_text="Enter description")


class FAQCardList(blocks.StructBlock):
    faq = blocks.ListBlock(FAQCard())       

    class Meta:
        template = "block/faq_page.html"
        icon = "edit"
        label = "FAQ List"


class CrousalHeader(blocks.StructBlock):
    images = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock(required=False)),]))
        
    class Meta:
        template = "block/CrousalHeader.html"
        icon = "doc-full"
        label = "Crousal Header Block"