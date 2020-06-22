from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks


# Orderable should be used to create our featured section

class HomePageBannerCarousel(Orderable):
    # ParentalKey references to the page(database table) this orderable should belong to
    # related_name will be used in the templates
    
    # Should be added to 'content_panels' to appear at Home page
    page = ParentalKey("home.HomePage", related_name='banner_carousel')
    
    # database model --> that references existing model
    banner_carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        # in case of False during migration you'll be asked to specify default value
        null=True,
        # There's always should be a banner image
        blank=False,
        on_delete=models.SET_NULL,
        # No special related name --> field name to be used
        related_name="+",
    )
    
    # Wagtail panel for admin
    panel = [
        ImageChooserPanel('banner_carousel_image')
    ]

class HomePage(Page):
    max_count = 1
    #appname.ModelName
    subpage_types = ['blog.BlogListingPage', 
    'contact.ContactPage', 
    'flex.FlexPage']
    
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    # will be displayed in the template as {{ self.banner_subtitle | richtext }}
    banner_sub = RichTextField(blank=True, null=True)

    # Foreign Key to the existing image model(database table) --> provides many-to-one relationship by adding a column 
    # to the local model to hold the remote value, basically by referencing wagtailimages.Images like this you receiving 
    # ready-to-use functionality for handling the images upload and management
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        # in case of False during migration you'll be asked to specify default value
        null=True,
        # There's always should be a banner image
        blank=False,
        on_delete=models.SET_NULL,
        # No special related name --> field name to be used
        related_name="+",
    )

    # Call to action
    # Foreign Key will automatically create a link to another web page from wagtail, instead of using direct link
    banner_cta = models.ForeignKey(
        # wagtailcore --> appname
        # Page --> model name 
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_sub'),
            InlinePanel("banner_carousel", max_num=5, min_num=1, label="Найголовніше"),
            PageChooserPanel("banner_cta"),
        ], heading="Заголовок" ),
        # MultiFieldPanel([
        #     InlinePanel("carousel", max_num=5, min_num=1, label="Найголовніше"),
        # ], heading="Додайте зображення"),
        StreamFieldPanel('content')
    ]

    class Meta:
        verbose_name = "My Home Page"
        verbose_name_plural = "Hommie Pages"





