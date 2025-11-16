from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q
from collections import Counter

from products.models import Product, Cart, CartItem
from quiz.models import Question, Option, UserAnswer


@login_required
def dashboard(request):
    """Simple dashboard showing counts and recent products."""
    user_count = User.objects.count()
    product_count = Product.objects.count()
    question_count = Question.objects.count()
    option_count = Option.objects.count()
    answer_count = UserAnswer.objects.count()

    recent_products = Product.objects.order_by('-id')[:6]

    context = {
        'user_count': user_count,
        'product_count': product_count,
        'question_count': question_count,
        'option_count': option_count,
        'answer_count': answer_count,
        'recent_products': recent_products,
        'today': timezone.now(),
    }

    return render(request, 'dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin/Brand dashboard with business insights and analytics"""
    
    # Basic counts
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_quizzes = UserAnswer.objects.values('user').distinct().count()
    total_cart_items = CartItem.objects.count()
    
    # Skin type distribution - most common skin types
    user_answers = UserAnswer.objects.all()
    skin_types_list = [answer.option.skin_type for answer in user_answers]
    skin_type_counter = Counter(skin_types_list)
    skin_type_distribution = [
        {'skin_type': skin_type.title(), 'count': count, 'percentage': round((count / len(skin_types_list) * 100), 1) if skin_types_list else 0}
        for skin_type, count in skin_type_counter.most_common()
    ]
    
    # Most recommended products (products for most common skin types)
    most_common_skin_types = [st for st, _ in skin_type_counter.most_common(3)]
    recommended_products = Product.objects.filter(
        skin_type__in=most_common_skin_types
    ).annotate(
        relevance_score=Count('skin_type')
    ).order_by('-relevance_score')[:10]
    
    # Products in cart - popularity metric
    products_in_cart = CartItem.objects.values('product__name', 'product__brand', 'product__skin_type').annotate(
        times_added=Count('id')
    ).order_by('-times_added')[:10]
    
    # Product type distribution
    product_types = Product.objects.values('product_type').annotate(
        count=Count('id')
    ).order_by('-count')[:8]
    
    # Products by skin type
    products_by_skin = Product.objects.values('skin_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent quiz activity
    recent_quiz_activity = UserAnswer.objects.select_related('user', 'question', 'option').order_by('-id')[:15]
    
    # User engagement metrics
    users_with_quizzes = UserAnswer.objects.values('user').distinct().count()
    users_with_carts = Cart.objects.filter(items__isnull=False).distinct().count()
    quiz_completion_rate = round((users_with_quizzes / total_users * 100), 1) if total_users > 0 else 0
    cart_usage_rate = round((users_with_carts / total_users * 100), 1) if total_users > 0 else 0
    
    # Top brands
    top_brands = Product.objects.values('brand').annotate(
        product_count=Count('id')
    ).order_by('-product_count')[:8]
    
    # Products needing attention (no image, no link, etc.)
    products_without_image = Product.objects.filter(Q(image='') | Q(image__isnull=True)).count()
    products_without_link = Product.objects.filter(Q(link='') | Q(link__isnull=True)).count()
    
    context = {
        # Basic metrics
        'total_users': total_users,
        'total_products': total_products,
        'total_quizzes': total_quizzes,
        'total_cart_items': total_cart_items,
        
        # Distributions
        'skin_type_distribution': skin_type_distribution,
        'product_types': product_types,
        'products_by_skin': products_by_skin,
        'top_brands': top_brands,
        
        # Popular items
        'recommended_products': recommended_products,
        'products_in_cart': products_in_cart,
        
        # Activity
        'recent_quiz_activity': recent_quiz_activity,
        
        # Engagement
        'quiz_completion_rate': quiz_completion_rate,
        'cart_usage_rate': cart_usage_rate,
        
        # Alerts
        'products_without_image': products_without_image,
        'products_without_link': products_without_link,
        
        'today': timezone.now(),
    }
    
    return render(request, 'admin_dashboard.html', context)

