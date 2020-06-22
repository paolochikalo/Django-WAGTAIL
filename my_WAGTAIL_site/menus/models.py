from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet

from pytils.translit import slugify

class MenuItem(Orderable):

    link_title = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    link_url = models.URLField(blank=True)
    link_page = models.ForeignKey(
        
        # With this class we will be able to select any page 
        # with for example blog.BlogDetailPage --> we will be able to select only blog pages
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    open_in_new_tab = models.BooleanField(default=False)

    page = ParentalKey("Menu", related_name='menu_items')

    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
        FieldPanel('open_in_new_tab')
    ]


@register_snippet
class Menu(ClusterableModel):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=slugify("title"), editable=True)
    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug')
        ], heading='Menu'),
        InlinePanel('menu_items', label="Menu Item")
    ]

    def __str__(self):
        return self.title
