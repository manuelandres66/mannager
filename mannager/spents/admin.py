from django.contrib import admin
from .models import Spent, SpentCategory
# Register your models here.
admin.site.register(Spent)
admin.site.register(SpentCategory)