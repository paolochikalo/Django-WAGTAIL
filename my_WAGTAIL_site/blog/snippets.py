
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from django.db import models



@register_snippet
class BlogAuthor(models.Model):

    name = models.CharField(max_length=150)
    profile = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            ImageChooserPanel('image'),
        ], heading="Профіль Автора"
        ),
        MultiFieldPanel([
            FieldPanel('profile'),
        ], heading="Соціальні мережі")
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Додайте Автора"
        verbose_name_plural = "Додайте Авторів"

@register_snippet
class BlogCategory(models.Model):
    
    name = models.CharField(max_length=150, verbose_name='Категорія', help_text='Вкажіть найменування категорії')
    slug = models.SlugField(verbose_name='URL', allow_unicode=True, max_length=150, help_text='Короткий URL для категорії')
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('icon')
    ]

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name
