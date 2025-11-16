from django.core.management.base import BaseCommand
from quiz.models import Question, Option


class Command(BaseCommand):
    help = 'Populate the database with sample quiz questions'

    def handle(self, *args, **kwargs):
        # Check if questions already exist
        if Question.objects.exists():
            self.stdout.write(self.style.WARNING('Questions already exist. Skipping...'))
            return

        # Question 1
        q1 = Question.objects.create(text="How does your skin feel after cleansing?")
        Option.objects.create(question=q1, text="Tight and dry", skin_type="dry")
        Option.objects.create(question=q1, text="Shiny and oily", skin_type="oily")
        Option.objects.create(question=q1, text="Oily in T-zone, dry on cheeks", skin_type="combination")
        Option.objects.create(question=q1, text="Uncomfortable and irritated", skin_type="sensitive")
        Option.objects.create(question=q1, text="Comfortable and balanced", skin_type="normal")

        # Question 2
        q2 = Question.objects.create(text="How often do you experience breakouts?")
        Option.objects.create(question=q2, text="Rarely or never", skin_type="dry")
        Option.objects.create(question=q2, text="Frequently, especially in T-zone", skin_type="oily")
        Option.objects.create(question=q2, text="Sometimes in oily areas", skin_type="combination")
        Option.objects.create(question=q2, text="Rarely, but skin reacts to products", skin_type="sensitive")
        Option.objects.create(question=q2, text="Occasionally", skin_type="normal")

        # Question 3
        q3 = Question.objects.create(text="How does your skin look by midday?")
        Option.objects.create(question=q3, text="Flaky or rough patches", skin_type="dry")
        Option.objects.create(question=q3, text="Shiny and greasy", skin_type="oily")
        Option.objects.create(question=q3, text="Shiny T-zone, dry cheeks", skin_type="combination")
        Option.objects.create(question=q3, text="Red or blotchy", skin_type="sensitive")
        Option.objects.create(question=q3, text="Fresh and even", skin_type="normal")

        # Question 4
        q4 = Question.objects.create(text="How does your skin react to new products?")
        Option.objects.create(question=q4, text="Absorbs quickly, needs more", skin_type="dry")
        Option.objects.create(question=q4, text="Feels heavy, causes breakouts", skin_type="oily")
        Option.objects.create(question=q4, text="Depends on the area", skin_type="combination")
        Option.objects.create(question=q4, text="Often causes redness or irritation", skin_type="sensitive")
        Option.objects.create(question=q4, text="Usually fine", skin_type="normal")

        # Question 5
        q5 = Question.objects.create(text="What is your main skin concern?")
        Option.objects.create(question=q5, text="Dryness and flaking", skin_type="dry")
        Option.objects.create(question=q5, text="Excess oil and large pores", skin_type="oily")
        Option.objects.create(question=q5, text="Uneven texture", skin_type="combination")
        Option.objects.create(question=q5, text="Redness and sensitivity", skin_type="sensitive")
        Option.objects.create(question=q5, text="Maintaining balance", skin_type="normal")

        self.stdout.write(self.style.SUCCESS('Successfully created 5 quiz questions with options!'))
