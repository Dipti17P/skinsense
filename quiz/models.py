from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)
    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
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
    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"


class SkinProgress(models.Model):
    """Track user's skin condition and satisfaction over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skin_progress')
    date = models.DateField(auto_now_add=True)
    
    # Satisfaction rating (1-10)
    satisfaction_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Rate your overall satisfaction (1-10)"
    )
    
    # Skin condition metrics (1-10 scale)
    hydration_level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="How hydrated does your skin feel? (1=Very dry, 10=Very hydrated)"
    )
    
    clarity = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Skin clarity/texture (1=Poor, 10=Excellent)"
    )
    
    breakouts = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Breakout frequency (1=Very frequent, 10=None)"
    )
    
    redness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Redness/irritation level (1=Very red, 10=No redness)"
    )
    
    # Optional notes
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about your skin today")
    
    # Current routine satisfaction
    routine_followed = models.BooleanField(default=True, help_text="Did you follow your routine today?")
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Skin Progress Entry'
        verbose_name_plural = 'Skin Progress Entries'
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    @property
    def overall_condition(self):
        """Calculate overall skin condition score"""
        return round((self.hydration_level + self.clarity + self.breakouts + self.redness) / 4, 1)
