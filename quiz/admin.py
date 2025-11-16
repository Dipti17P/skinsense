from django.contrib import admin
from .models import Question, Option, UserAnswer, SkinProgress

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserAnswer)

@admin.register(SkinProgress)
class SkinProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'satisfaction_rating', 'overall_condition', 'routine_followed']
    list_filter = ['date', 'routine_followed', 'satisfaction_rating']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'
