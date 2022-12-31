from django.contrib import admin

from .models import (
    Question,
    Form,
    Client,
    Answer,
    Record
)

admin.site.register(Question)
admin.site.register(Form)
admin.site.register(Client)
admin.site.register(Answer)
admin.site.register(Record)
