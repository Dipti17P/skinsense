from django.contrib import admin
from .models import Product, Cart, CartItem, ProductReview, UserRoutine, RoutineStep, SkincareReminder

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'get_total_items']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

class RoutineStepInline(admin.TabularInline):
    model = RoutineStep
    extra = 1

@admin.register(SkincareReminder)
class SkincareReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'reminder_type', 'time', 'frequency', 'is_active', 'created_at']
    list_filter = ['reminder_type', 'frequency', 'is_active', 'created_at']
    search_fields = ['user__username', 'title', 'notes']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'title', 'would_recommend', 'helpful_count', 'created_at']
    list_filter = ['rating', 'would_recommend', 'skin_type', 'created_at']
    search_fields = ['title', 'review_text', 'user__username', 'product__name']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']

@admin.register(UserRoutine)
class UserRoutineAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'skin_type', 'routine_type', 'likes_count', 'views_count', 'is_public', 'created_at']
    list_filter = ['skin_type', 'routine_type', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['likes_count', 'views_count', 'created_at', 'updated_at']
    inlines = [RoutineStepInline]
    filter_horizontal = ['products']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'product_type', 'skin_type', 'price', 'image']
    list_filter = ['product_type', 'skin_type', 'brand']
    search_fields = ['name', 'brand', 'description']
    list_editable = ['price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'product_type', 'skin_type')
        }),
        ('Details', {
            'fields': ('description', 'image', 'price')
        }),
    )

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)