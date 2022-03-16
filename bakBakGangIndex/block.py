from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class BBGTestimonialSection(blocks.StructBlock):
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/sectiontestimonial.html"
        icon = "placeholder"
        label = "Section Testimonial"



class BBGCards1Section(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/cards1.html"
        icon = "placeholder"
        label = "Section cards1"



class BBGCards2Section(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/cards2.html"
        icon = "placeholder"
        label = "Section cards2"




class BBGCardFooterSection(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/bolBahen_footer_card.html"
        icon = "placeholder"
        label = "Section cards2"


class BBG2TestimonialSection(blocks.StructBlock):
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/bolBahen_section_2_cardtestimonial.html"
        icon = "placeholder"
        label = "Section Testimonial"


class BolbehanSection3Cards(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/bolbehan_section_3_cards.html"
        icon = "placeholder"
        label = "Section cards1"


class BolbehanSection4Cards(blocks.StructBlock):
    order_by = blocks.CharBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    

    class Meta:
        template = "bakBakGangIndex/block/bolbehan_section_4_cards.html"
        icon = "placeholder"
        label = "Section cards2"

