from django.contrib import admin
from .models import TestSummary,TestCase

# Register your models here.
admin.site.register(TestSummary)
admin.site.register(TestCase)