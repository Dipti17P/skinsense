from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    product_type = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in INR", null=True, blank=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"


class SkincareReminder(models.Model):
    """Reminders for skincare routines"""
    REMINDER_TYPES = [
        ('morning', 'Morning Routine'),
        ('evening', 'Evening Routine'),
        ('both', 'Both Morning & Evening'),
        ('custom', 'Custom Time'),
    ]
    
    DAYS_OF_WEEK = [
        ('daily', 'Daily'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('custom', 'Custom Days'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skincare_reminders')
    title = models.CharField(max_length=200, default="Skincare Routine")
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, default='morning')
    time = models.TimeField(help_text="Time for reminder")
    frequency = models.CharField(max_length=20, choices=DAYS_OF_WEEK, default='daily')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Additional notes or steps")
    
    # Custom days (if frequency is 'custom')
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['time']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} at {self.time}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.user.username}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        unique_together = ('cart', 'product')


class ProductReview(models.Model):
    """User reviews for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], help_text="Rating 1-5 stars")
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    skin_type = models.CharField(max_length=20, help_text="Your skin type")
    
    # Effectiveness ratings
    effectiveness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    value_for_money = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    
    # Usage details
    usage_duration = models.CharField(max_length=50, help_text="How long have you used this?")
    would_recommend = models.BooleanField(default=True)
    
    # Engagement
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"


class UserRoutine(models.Model):
    """User-shared skincare routines"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    title = models.CharField(max_length=200)
    description = models.TextField()
    skin_type = models.CharField(
        max_length=20,
        choices=[
            ('dry', 'Dry'),
            ('oily', 'Oily'),
            ('combination', 'Combination'),
            ('sensitive', 'Sensitive'),
            ('normal', 'Normal')
        ]
    )
    routine_type = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('night', 'Night'),
            ('both', 'Morning & Night')
        ]
    )
    
    # Products used (optional references)
    products = models.ManyToManyField(Product, blank=True, related_name='used_in_routines')
    
    # Engagement
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Visibility
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class RoutineStep(models.Model):
    """Individual steps in a user routine"""
    routine = models.ForeignKey(UserRoutine, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    step_name = models.CharField(max_length=100)
    instructions = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"{self.routine.title} - Step {self.step_number}"


class ReviewHelpful(models.Model):
    """Track users who found reviews helpful"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('review', 'user')


class RoutineLike(models.Model):
    """Track users who liked routines"""
    routine = models.ForeignKey(UserRoutine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('routine', 'user')
