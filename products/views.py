from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, ProductReview, UserRoutine, RoutineStep, ReviewHelpful, RoutineLike, SkincareReminder
from django.db.models import Avg, Count, Q
from decimal import Decimal
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

def product_list(request):
    products = Product.objects.all()
    
    # Filter by skin type if provided
    skin_type = request.GET.get('skin_type')
    if skin_type:
        products = products.filter(skin_type=skin_type)
    
    # Get cart item count for logged-in users
    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.get_total_items()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # If item already exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity in cart!')
    else:
        messages.success(request, f'{product.name} added to cart!')
    
    # Redirect back to the page they came from
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    return render(request, 'products/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Quantity updated!')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, 'Quantity updated!')
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart!')
        elif action == 'remove':
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('view_cart')


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared!')
    return redirect('view_cart')


@login_required
def checkout(request):
    """Checkout page with Razorpay payment"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    # Calculate total
    subtotal = sum(item.product.price * item.quantity for item in cart_items if item.product.price)
    tax = subtotal * Decimal('0.18')  # 18% GST
    total = subtotal + tax
    
    # Check if Razorpay keys are configured
    demo_mode = False
    razorpay_order_id = 'demo_order_' + str(request.user.id)
    razorpay_key_id = 'demo_key'
    
    if (hasattr(settings, 'RAZORPAY_KEY_ID') and 
        hasattr(settings, 'RAZORPAY_KEY_SECRET') and
        'your_key' not in settings.RAZORPAY_KEY_ID.lower() and 
        'your_key' not in settings.RAZORPAY_KEY_SECRET.lower()):
        
        try:
            # Create Razorpay order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Convert to paise (Razorpay uses smallest currency unit)
            amount_in_paise = int(total * 100)
            
            razorpay_order = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': '1'
            })
            
            razorpay_order_id = razorpay_order['id']
            razorpay_key_id = settings.RAZORPAY_KEY_ID
            
        except razorpay.errors.BadRequestError as e:
            messages.warning(request, '⚠️ Running in Demo Mode - Razorpay not configured')
            demo_mode = True
        except Exception as e:
            messages.warning(request, f'⚠️ Running in Demo Mode - {str(e)}')
            demo_mode = True
    else:
        messages.info(request, '🛠️ Demo Mode Active - Configure Razorpay keys in settings.py for real payments')
        demo_mode = True
    
    return render(request, 'products/checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_key_id': razorpay_key_id,
        'amount_in_paise': int(total * 100),
        'user_name': request.user.get_full_name() or request.user.username,
        'user_email': request.user.email,
        'demo_mode': demo_mode,
    })


@csrf_exempt
def process_payment(request):
    """Process Razorpay payment verification"""
    if request.method == 'POST':
        # Check for demo mode
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        
        if order_id.startswith('demo_order_') or payment_id.startswith('demo_pay_'):
            # Demo mode - simulate successful payment
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart.items.all().delete()
            
            messages.success(request, f'🎉 Demo Payment Successful! Order ID: {order_id}')
            return redirect('payment_success', order_id=payment_id or order_id)
        
        try:
            # Real Razorpay payment verification
            signature = request.POST.get('razorpay_signature')
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # Verify signature
            client.utility.verify_payment_signature(params_dict)
            
            # Payment is successful
            cart = get_object_or_404(Cart, user=request.user)
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, f'🎉 Payment Successful! Payment ID: {payment_id}')
            return redirect('payment_success', order_id=payment_id)
            
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, '❌ Payment verification failed! Please try again.')
            return redirect('checkout')
        except Exception as e:
            messages.error(request, f'❌ Payment failed: {str(e)}')
            return redirect('checkout')
    
    return redirect('checkout')


@login_required
def payment_success(request, order_id):
    """Payment success page"""
    return render(request, 'products/payment_success.html', {
        'order_id': order_id
    })


# Community Features

def community_hub(request):
    """Main community page with reviews and routines"""
    # Get recent reviews
    recent_reviews = ProductReview.objects.select_related('user', 'product').all()[:10]
    
    # Get popular routines
    popular_routines = UserRoutine.objects.filter(is_public=True).select_related('user').order_by('-likes_count', '-views_count')[:8]
    
    # Get top rated products
    top_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:6]
    
    # Statistics
    stats = {
        'total_reviews': ProductReview.objects.count(),
        'total_routines': UserRoutine.objects.filter(is_public=True).count(),
        'total_members': ProductReview.objects.values('user').distinct().count()
    }
    
    context = {
        'recent_reviews': recent_reviews,
        'popular_routines': popular_routines,
        'top_products': top_products,
        'stats': stats
    }
    
    return render(request, 'products/community_hub.html', context)


@login_required
def add_review(request, product_id):
    """Add a product review"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed this product
    existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        if existing_review:
            messages.warning(request, 'You have already reviewed this product!')
            return redirect('community_hub')
        
        try:
            review = ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=int(request.POST.get('rating')),
                title=request.POST.get('title'),
                review_text=request.POST.get('review_text'),
                skin_type=request.POST.get('skin_type'),
                effectiveness=int(request.POST.get('effectiveness')),
                value_for_money=int(request.POST.get('value_for_money')),
                usage_duration=request.POST.get('usage_duration'),
                would_recommend=request.POST.get('would_recommend') == 'on'
            )
            messages.success(request, '✅ Review posted successfully!')
            return redirect('community_hub')
        except Exception as e:
            messages.error(request, f'Error posting review: {str(e)}')
    
    context = {
        'product': product,
        'existing_review': existing_review
    }
    return render(request, 'products/add_review.html', context)


@login_required
def mark_helpful(request, review_id):
    """Mark a review as helpful"""
    review = get_object_or_404(ProductReview, id=review_id)
    
    helpful, created = ReviewHelpful.objects.get_or_create(
        review=review,
        user=request.user
    )
    
    if created:
        review.helpful_count += 1
        review.save()
        messages.success(request, 'Thanks for your feedback!')
    else:
        messages.info(request, 'You already marked this as helpful!')
    
    return redirect('community_hub')


@login_required
def share_routine(request):
    """Share a new skincare routine"""
    if request.method == 'POST':
        try:
            routine = UserRoutine.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                skin_type=request.POST.get('skin_type'),
                routine_type=request.POST.get('routine_type'),
                is_public=request.POST.get('is_public') == 'on'
            )
            
            # Add steps
            step_count = int(request.POST.get('step_count', 0))
            for i in range(1, step_count + 1):
                step_name = request.POST.get(f'step_name_{i}')
                step_instructions = request.POST.get(f'step_instructions_{i}')
                product_id = request.POST.get(f'step_product_{i}')
                
                if step_name and step_instructions:
                    step = RoutineStep.objects.create(
                        routine=routine,
                        step_number=i,
                        step_name=step_name,
                        instructions=step_instructions
                    )
                    if product_id:
                        try:
                            product = Product.objects.get(id=int(product_id))
                            step.product = product
                            step.save()
                        except:
                            pass
            
            messages.success(request, '✅ Routine shared successfully!')
            return redirect('community_hub')
        except Exception as e:
            messages.error(request, f'Error sharing routine: {str(e)}')
    
    products = Product.objects.all()
    return render(request, 'products/share_routine.html', {'products': products})


@login_required
def view_routine(request, routine_id):
    """View detailed routine"""
    routine = get_object_or_404(UserRoutine, id=routine_id)
    
    # Increment views
    routine.views_count += 1
    routine.save(update_fields=['views_count'])
    
    # Check if user liked this
    user_liked = RoutineLike.objects.filter(routine=routine, user=request.user).exists() if request.user.is_authenticated else False
    
    steps = routine.steps.all()
    
    context = {
        'routine': routine,
        'steps': steps,
        'user_liked': user_liked
    }
    return render(request, 'products/view_routine.html', context)


@login_required
def like_routine(request, routine_id):
    """Like/unlike a routine"""
    routine = get_object_or_404(UserRoutine, id=routine_id)
    
    like, created = RoutineLike.objects.get_or_create(
        routine=routine,
        user=request.user
    )
    
    if created:
        routine.likes_count += 1
        routine.save()
        messages.success(request, '❤️ Routine liked!')
    else:
        like.delete()
        routine.likes_count = max(0, routine.likes_count - 1)
        routine.save()
        messages.info(request, 'Routine unliked')
    
    return redirect('view_routine', routine_id=routine_id)


# Skincare Reminders

@login_required
def reminder_list(request):
    """List all reminders for the user"""
    reminders = SkincareReminder.objects.filter(user=request.user)
    return render(request, 'products/reminders.html', {'reminders': reminders})


@login_required
def add_reminder(request):
    """Add a new skincare reminder"""
    if request.method == 'POST':
        try:
            reminder = SkincareReminder.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                reminder_type=request.POST.get('reminder_type'),
                time=request.POST.get('time'),
                frequency=request.POST.get('frequency'),
                notes=request.POST.get('notes', ''),
                monday=request.POST.get('monday') == 'on',
                tuesday=request.POST.get('tuesday') == 'on',
                wednesday=request.POST.get('wednesday') == 'on',
                thursday=request.POST.get('thursday') == 'on',
                friday=request.POST.get('friday') == 'on',
                saturday=request.POST.get('saturday') == 'on',
                sunday=request.POST.get('sunday') == 'on',
            )
            messages.success(request, '⏰ Reminder created successfully!')
            return redirect('reminder_list')
        except Exception as e:
            messages.error(request, f'Error creating reminder: {str(e)}')
    
    return render(request, 'products/add_reminder.html')


@login_required
def edit_reminder(request, reminder_id):
    """Edit an existing reminder"""
    reminder = get_object_or_404(SkincareReminder, id=reminder_id, user=request.user)
    
    if request.method == 'POST':
        try:
            reminder.title = request.POST.get('title')
            reminder.reminder_type = request.POST.get('reminder_type')
            reminder.time = request.POST.get('time')
            reminder.frequency = request.POST.get('frequency')
            reminder.notes = request.POST.get('notes', '')
            reminder.monday = request.POST.get('monday') == 'on'
            reminder.tuesday = request.POST.get('tuesday') == 'on'
            reminder.wednesday = request.POST.get('wednesday') == 'on'
            reminder.thursday = request.POST.get('thursday') == 'on'
            reminder.friday = request.POST.get('friday') == 'on'
            reminder.saturday = request.POST.get('saturday') == 'on'
            reminder.sunday = request.POST.get('sunday') == 'on'
            reminder.save()
            messages.success(request, '✅ Reminder updated!')
            return redirect('reminder_list')
        except Exception as e:
            messages.error(request, f'Error updating reminder: {str(e)}')
    
    return render(request, 'products/edit_reminder.html', {'reminder': reminder})


@login_required
def toggle_reminder(request, reminder_id):
    """Toggle reminder active status"""
    reminder = get_object_or_404(SkincareReminder, id=reminder_id, user=request.user)
    reminder.is_active = not reminder.is_active
    reminder.save()
    
    status = 'activated' if reminder.is_active else 'deactivated'
    messages.success(request, f'⏰ Reminder {status}!')
    return redirect('reminder_list')


@login_required
def delete_reminder(request, reminder_id):
    """Delete a reminder"""
    reminder = get_object_or_404(SkincareReminder, id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, '🗑️ Reminder deleted!')
    return redirect('reminder_list')
