from django.contrib import admin
from .models import Spent, SpentCategory, Earn, EarnCategory, Account, SubCash
# Register your models here.

class SubCashAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SubCash._meta.get_fields()]


admin.site.register(Book, BookAdmin)
admin.site.register(Spent)
admin.site.register(SpentCategory)
admin.site.register(Earn)
admin.site.register(EarnCategory)
admin.site.register(Account)
admin.site.register(SubCash, SubCashAdmin)