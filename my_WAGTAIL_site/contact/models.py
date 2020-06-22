from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )

class ContactPage(AbstractEmailForm):
    template = 'contact/contact_page.html'
    intro = RichTextField(blank=True)
    thank_you = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Field'),
        FieldPanel('thank_you', heading='Текст відповідь'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col-6', heading='Від кого'),
                FieldPanel('to_address', classname='col-6', heading='Кому'),
            ]),
            FieldPanel('subject', heading='Тема'),
        ], heading="Налаштуйте Email")
    ]