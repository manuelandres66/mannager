from django.contrib import admin
from .models import Spent, SpentCategory, Earn, EarnCategory
# Register your models here.
admin.site.register(Spent)
admin.site.register(SpentCategory)
admin.site.register(Earn)
admin.site.register(EarnCategory)