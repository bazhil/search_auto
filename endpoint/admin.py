# coding: utf-8
from django.contrib import admin
from .models import Venicle, Categories
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class VenicleResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Categories, 'category'))

    class Meta:
        model = Venicle


class VenicleAdmin(ImportExportModelAdmin):
    resource_class = VenicleResource
    list_display = ['mark', 'model', 'category', 'reg_number', 'issue_year', 'vin', 'sts_number', 'sts_date', 'description']
    inlines = []

admin.site.register(Venicle, VenicleAdmin)
admin.site.register(Categories)
# Register your models here.

