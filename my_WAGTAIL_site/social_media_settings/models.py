from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

@register_setting
class SocialMediaSettings(BaseSetting):

    facebook = models.URLField(blank=True, null=True, help_text='Напишіть нам у Facebook')
    youtube = models.URLField(blank=True, null=True, help_text='Наш YouTube канал')
    twitter = models.URLField(blank=True, null=True, help_text='Будьте в курсі останніх подій з нами в Twitter')
    instagram = models.URLField(blank=True, null=True, help_text='Слідкуйте за нами в Instagram')

    #panels is how things displayed in Wagtail
    panels=[
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("youtube"),
            FieldPanel("twitter"),
            FieldPanel("instagram")
        ], heading="Наші аккаунти в соціяльних медіа")

    ]