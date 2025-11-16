from django.shortcuts import render, redirect
from .models import Question, Option, UserAnswer, SkinProgress
from products.models import Product
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse

@login_required(login_url='/accounts/login/')
def start_quiz(request):
    # Clear previous answers for this user
    UserAnswer.objects.filter(user=request.user).delete()
    
    # Get first question
    first_question = Question.objects.order_by('id').first()
    if first_question:
        return redirect('quiz_question', qid=first_question.id)
    else:
        messages.error(request, "No questions found in the quiz.")
        return redirect('dashboard')

@login_required(login_url='/accounts/login/')
def quiz_question(request, qid):
    try:
        question = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        return redirect('quiz_result')

    # Calculate progress
    all_questions = Question.objects.order_by('id')
    total_questions = all_questions.count()
    current_number = list(all_questions.values_list('id', flat=True)).index(question.id) + 1
    progress_percentage = int((current_number / total_questions) * 100) if total_questions > 0 else 0

    if request.method == 'POST':
        option_id = request.POST.get('option')
        if option_id:
            # Save answer (update if already exists)
            UserAnswer.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'option_id': option_id}
            )

            # Redirect to next question or result
            next_question = Question.objects.filter(id__gt=question.id).order_by('id').first()
            if next_question:
                return redirect('quiz_question', qid=next_question.id)
            else:
                return redirect('quiz_result')
        else:
            messages.warning(request, "Please select an option before proceeding.")

    return render(request, 'quiz/question.html', {
        'question': question,
        'current_number': current_number,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage
    })

@login_required(login_url='/accounts/login/')
def quiz_result(request):
    # Get user answers
    answers = UserAnswer.objects.filter(user=request.user)

    if not answers.exists():
        messages.warning(request, "No answers found. Please start the quiz first.")
        return redirect('quiz_start')

    # Calculate most common skin type
    skin_types = [a.option.skin_type for a in answers]
    skin_type = Counter(skin_types).most_common(1)[0][0]

    # Get products for the skin type
    products = Product.objects.filter(skin_type=skin_type)

    # Generate skincare routines based on skin type
    routines = generate_routine(skin_type, products)

    return render(request, 'quiz/result.html', {
        'skin_type': skin_type,
        'products': products,
        'morning_routine': routines['morning'],
        'night_routine': routines['night'],
    })

def generate_routine(skin_type, products):
    """Generate personalized morning and night skincare routines"""
    
    # Organize products by type
    product_types = {
        'cleanser': products.filter(product_type__icontains='Cleanser').first(),
        'toner': products.filter(product_type__icontains='Toner').first(),
        'serum': products.filter(product_type__icontains='Serum').first(),
        'moisturizer': products.filter(product_type__icontains='Moisturizer').first() or products.filter(product_type__icontains='Cream').first(),
        'sunscreen': products.filter(product_type__icontains='Sunscreen').first() or products.filter(product_type__icontains='SPF').first(),
        'mask': products.filter(product_type__icontains='Mask').first(),
    }

    # Skin type specific recommendations
    skin_tips = {
        'dry': {
            'focus': 'Hydration and moisture retention',
            'avoid': 'Harsh cleansers and alcohol-based products',
            'key_ingredients': 'Hyaluronic acid, Ceramides, Glycerin',
        },
        'oily': {
            'focus': 'Oil control and pore refinement',
            'avoid': 'Heavy creams and comedogenic oils',
            'key_ingredients': 'Salicylic acid, Niacinamide, Tea tree oil',
        },
        'combination': {
            'focus': 'Balance hydration and oil control',
            'avoid': 'Products that are too harsh or too heavy',
            'key_ingredients': 'Hyaluronic acid, Niacinamide, Vitamin C',
        },
        'sensitive': {
            'focus': 'Gentle care and barrier protection',
            'avoid': 'Fragrances, harsh acids, and irritants',
            'key_ingredients': 'Centella, Ceramides, Aloe vera',
        },
        'normal': {
            'focus': 'Maintaining balance and prevention',
            'avoid': 'Over-exfoliation and harsh treatments',
            'key_ingredients': 'Vitamin C, Hyaluronic acid, Antioxidants',
        },
    }

    # Morning routine
    morning_routine = {
        'title': 'Morning Skincare Routine',
        'subtitle': 'Start your day with fresh, protected skin',
        'total_time': '8-10 minutes',
        'steps': [
            {
                'step': 1,
                'name': 'Gentle Cleanser',
                'time': '1-2 min',
                'icon': '💧',
                'instructions': 'Wash your face with lukewarm water and a gentle cleanser. Massage in circular motions for 60 seconds.',
                'product': product_types['cleanser'],
                'tip': 'Use lukewarm water, not hot, to avoid stripping natural oils.'
            },
            {
                'step': 2,
                'name': 'Toner (Optional)',
                'time': '30 sec',
                'icon': '✨',
                'instructions': 'Apply toner with a cotton pad or pat gently with hands to balance pH and prep skin.',
                'product': product_types['toner'],
                'tip': 'Pat, don\'t rub! This helps with better absorption.'
            },
            {
                'step': 3,
                'name': 'Serum/Treatment',
                'time': '1 min',
                'icon': '💎',
                'instructions': 'Apply 2-3 drops of serum to face and neck. Press gently into skin.',
                'product': product_types['serum'],
                'tip': f"Focus on {skin_tips.get(skin_type, {}).get('key_ingredients', 'beneficial ingredients')}."
            },
            {
                'step': 4,
                'name': 'Moisturizer',
                'time': '1-2 min',
                'icon': '🌸',
                'instructions': 'Apply moisturizer evenly to lock in hydration. Use upward motions.',
                'product': product_types['moisturizer'],
                'tip': 'Wait 1 minute before applying sunscreen for better absorption.'
            },
            {
                'step': 5,
                'name': 'Sunscreen (SPF 30+)',
                'time': '1-2 min',
                'icon': '☀️',
                'instructions': 'Apply generous amount of sunscreen (2 finger lengths) to face and neck. Wait 15 min before sun exposure.',
                'product': product_types['sunscreen'],
                'tip': 'Reapply every 2 hours if outdoors! This is the most important step.'
            },
        ],
        'tips': skin_tips.get(skin_type, {})
    }

    # Night routine
    night_routine = {
        'title': 'Night Skincare Routine',
        'subtitle': 'Repair and rejuvenate while you sleep',
        'total_time': '10-15 minutes',
        'steps': [
            {
                'step': 1,
                'name': 'Double Cleanse',
                'time': '2-3 min',
                'icon': '🧼',
                'instructions': 'First, remove makeup/sunscreen with cleansing oil/balm. Then, use your regular cleanser to deep clean.',
                'product': product_types['cleanser'],
                'tip': 'Double cleansing ensures all impurities are removed for better overnight repair.'
            },
            {
                'step': 2,
                'name': 'Toner',
                'time': '30 sec',
                'icon': '✨',
                'instructions': 'Apply toner to rebalance and prepare skin for treatments.',
                'product': product_types['toner'],
                'tip': 'Use a hydrating toner at night for extra nourishment and repair.'
            },
            {
                'step': 3,
                'name': 'Night Serum/Treatment',
                'time': '1-2 min',
                'icon': '🌟',
                'instructions': 'Apply treatment serums targeting your specific concerns (anti-aging, brightening, etc.).',
                'product': product_types['serum'],
                'tip': 'Night is best for active ingredients like retinol and AHAs that work while you sleep.'
            },
            {
                'step': 4,
                'name': 'Night Cream',
                'time': '1-2 min',
                'icon': '🌙',
                'instructions': 'Apply a richer night cream to support skin repair and regeneration overnight.',
                'product': product_types['moisturizer'],
                'tip': 'Night creams are typically thicker and more nourishing to lock in moisture.'
            },
            {
                'step': 5,
                'name': 'Weekly Mask (2-3x)',
                'time': '15-20 min',
                'icon': '🎭',
                'instructions': 'Use a treatment mask 2-3 times per week after cleansing. Follow with serum and moisturizer.',
                'product': product_types['mask'],
                'tip': 'Do this step 2-3 times per week, not daily. Perfect for relaxing before bed.'
            },
        ],
        'tips': skin_tips.get(skin_type, {})
    }

    return {
        'morning': morning_routine,
        'night': night_routine,
    }


@login_required(login_url='/accounts/login/')
def track_progress(request):
    """View and add progress tracking entries"""
    if request.method == 'POST':
        # Save new progress entry
        try:
            progress = SkinProgress.objects.create(
                user=request.user,
                satisfaction_rating=int(request.POST.get('satisfaction_rating')),
                hydration_level=int(request.POST.get('hydration_level')),
                clarity=int(request.POST.get('clarity')),
                breakouts=int(request.POST.get('breakouts')),
                redness=int(request.POST.get('redness')),
                routine_followed=request.POST.get('routine_followed') == 'on',
                notes=request.POST.get('notes', '')
            )
            messages.success(request, '✅ Progress entry saved successfully!')
            return redirect('track_progress')
        except Exception as e:
            messages.error(request, f'Error saving progress: {str(e)}')
    
    # Get user's progress entries
    progress_entries = SkinProgress.objects.filter(user=request.user).order_by('-date')[:30]
    
    # Prepare chart data
    chart_data = {
        'dates': [],
        'satisfaction': [],
        'hydration': [],
        'clarity': [],
        'breakouts': [],
        'redness': [],
        'overall': []
    }
    
    for entry in reversed(progress_entries):
        chart_data['dates'].append(entry.date.strftime('%b %d'))
        chart_data['satisfaction'].append(entry.satisfaction_rating)
        chart_data['hydration'].append(entry.hydration_level)
        chart_data['clarity'].append(entry.clarity)
        chart_data['breakouts'].append(entry.breakouts)
        chart_data['redness'].append(entry.redness)
        chart_data['overall'].append(entry.overall_condition)
    
    # Calculate statistics
    stats = {}
    if progress_entries.exists():
        stats['avg_satisfaction'] = round(sum([e.satisfaction_rating for e in progress_entries]) / len(progress_entries), 1)
        stats['avg_condition'] = round(sum([e.overall_condition for e in progress_entries]) / len(progress_entries), 1)
        stats['total_entries'] = len(progress_entries)
        stats['routine_compliance'] = round(sum([1 for e in progress_entries if e.routine_followed]) / len(progress_entries) * 100, 1)
        
        # Calculate trend (comparing first half vs second half)
        mid_point = len(progress_entries) // 2
        if mid_point > 0:
            recent_avg = round(sum([e.satisfaction_rating for e in list(progress_entries)[:mid_point]]) / mid_point, 1)
            older_avg = round(sum([e.satisfaction_rating for e in list(progress_entries)[mid_point:]]) / len(list(progress_entries)[mid_point:]), 1)
            stats['trend'] = 'improving' if recent_avg > older_avg else 'stable' if recent_avg == older_avg else 'declining'
            stats['trend_diff'] = round(abs(recent_avg - older_avg), 1)
    
    # Check if user logged today
    today_entry = SkinProgress.objects.filter(user=request.user, date=timezone.now().date()).exists()
    
    context = {
        'progress_entries': progress_entries,
        'chart_data_json': json.dumps(chart_data),
        'stats': stats,
        'today_entry': today_entry,
    }
    
    return render(request, 'quiz/track_progress.html', context)



