from wagtail.core import blocks

class Testimonial(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Enter title")


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
