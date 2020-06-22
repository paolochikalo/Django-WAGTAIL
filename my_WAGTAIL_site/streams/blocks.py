from wagtail.core import blocks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock


"""
In StreamFields we don't use Django models. instead we use Wagtail blocks.
"""

class TitleAndTextBlock(blocks.StructBlock):
    """ Title and Text and nothing else """
    # models.CharField --> blocks.CharBlock
    title = blocks.CharBlock(required=True,
                             help_text="*ОБОВ'ЯЗКОВО Заголовок статті")
    text = blocks.TextBlock(required=True,
                            help_text="*ОБОВ'ЯЗКОВО Текст статті")

    class Meta:  #noqa
        template = "streams/title_and_text.html"
        icon = "doc-full"
        label = "Title & Text"


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "streams/my_richtext_block.html"
        icon = "edit"
        label = "Додати Статтю"


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Заголовок універсальної картки")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text="If the button page above is selected, that will be used first.",  # noqa
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Універсальна картка"


class CTABlock(blocks.StructBlock):
    
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True)
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Дізнатися більше", max_length=45)

    class Meta:
        template ="streams/cta_blocks.html"
        icon = "placeholder"
        label = "Заклик до дії"


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue