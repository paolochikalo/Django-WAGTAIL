from django.db import models

class Subscribers(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False, help_text='Вкажіть свій email')
    full_name = models.CharField(max_length=100, blank=False, null=False, help_text='Імʼя та фамілія')

    def __str__(self):
        return self.full_name + " : "+ self.email

    class Meta:
        verbose_name = 'Підписник'
        verbose_name_plural = 'Підписники'