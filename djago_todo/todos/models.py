from django.db import models

class ToDo(models.Model):
    content = models.TextField(max_length=120)
