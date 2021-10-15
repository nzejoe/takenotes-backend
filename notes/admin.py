from django.contrib import admin
from .models import Label, Note

class LabelAdmin(admin.ModelAdmin):
    model = Label
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug']

admin.site.register(Label, LabelAdmin)
admin.site.register(Note)
