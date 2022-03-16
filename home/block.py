from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class SimpleCrousal(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=True, help_text="Crousal title")
    image = ImageChooserBlock(required=False)
    bg_color = blocks.CharBlock(max_length=100, required=True, help_text="Background Color in HEX value")
    text_color = blocks.CharBlock(max_length=100, required=True, help_text="Text Color in HEX value")

    description = blocks.ListBlock(blocks.StructBlock([
        ("description",blocks.RichTextBlock(required=False))
    ]))

    class Meta:
        template = "home/SimpleCrousal.html"
        icon = "placeholder"
        label = "Simple Crousal Block"


class AdvanceCrousal(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=True, help_text=" Add crousal title")
    cards = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock(required=False)),
        ("title",blocks.CharBlock(required=False)),
        ("description",blocks.RichTextBlock(required=False)),
    ]))

    class Meta:
        template = "home/AdvanceCrousal.html"
        icon = "doc-full"
        label = "Advance Crousal Block"


class TermPageCard(blocks.StructBlock):
    serial_number = blocks.CharBlock(required=True, help_text="Add Serial Number")
    serial_bg_color = blocks.CharBlock(required=True, help_text="Add Serial Background Color in HEX value")
    serial_text_color = blocks.CharBlock(required=True, help_text="Add Serial Text Color in HEX value")
    description = blocks.RichTextBlock(required=False, help_text="Add description")
    bg_color = blocks.CharBlock(required=True, help_text="Add Background Color in HEX value",
                                blank=True, null=True, default="#FFFFFF")


    class Meta:
        template = "home/term_page_card.html"
        icon = "edit"
        label = "Term-Page Card"

