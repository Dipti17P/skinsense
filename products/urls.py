from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/<str:order_id>/', views.payment_success, name='payment_success'),
    
    # Community features
    path('community/', views.community_hub, name='community_hub'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    path('review/helpful/<int:review_id>/', views.mark_helpful, name='mark_helpful'),
    path('routine/share/', views.share_routine, name='share_routine'),
    path('routine/<int:routine_id>/', views.view_routine, name='view_routine'),
    path('routine/like/<int:routine_id>/', views.like_routine, name='like_routine'),
    
    # Skincare reminders
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/add/', views.add_reminder, name='add_reminder'),
    path('reminders/edit/<int:reminder_id>/', views.edit_reminder, name='edit_reminder'),
    path('reminders/toggle/<int:reminder_id>/', views.toggle_reminder, name='toggle_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
]
