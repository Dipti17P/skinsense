from django.core.management.base import BaseCommand
from products.models import Product
from django.core.files.base import ContentFile
import requests


class Command(BaseCommand):
    help = 'Add placeholder images to products using image URLs'

    def handle(self, *args, **kwargs):
        # Image URLs for different product types (using Unsplash placeholder images)
        product_images = {
            'Hydrating Facial Cleanser': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&q=80',
            'Ultra Facial Cream': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&q=80',
            'Toleriane Double Repair Face Moisturizer': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400&q=80',
            'Midnight Recovery Concentrate': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&q=80',
            'Foaming Facial Cleanser': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&q=80',
            'Effaclar Duo Dual Action Acne Treatment': 'https://images.unsplash.com/photo-1620916297754-0a2c2e59b76b?w=400&q=80',
            'Oil-Free Acne Moisturizer': 'https://images.unsplash.com/photo-1570194065650-d99fb4d1e93b?w=400&q=80',
            'Niacinamide 10% + Zinc 1%': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&q=80',
            'Supermud Clearing Treatment': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&q=80',
            'Dramatically Different Moisturizing Gel': 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=400&q=80',
            'Daily Microfoliant': 'https://images.unsplash.com/photo-1570194065650-d99fb4d1e93b?w=400&q=80',
            'Hydro Boost Water Gel': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&q=80',
            'Multi-Active Day Cream': 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&q=80',
            'Ultra Gentle Hydrating Cleanser': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&q=80',
            'Cicaplast Baume B5': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400&q=80',
            'Skin Recovery Cream': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&q=80',
            'Redness Relief SPF 30': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&q=80',
            'Take The Day Off Cleansing Balm': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&q=80',
            'Moisture Surge 100H Auto-Replenishing Hydrator': 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=400&q=80',
            'Vitamin C Serum': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&q=80',
            'Advanced Night Repair': 'https://images.unsplash.com/photo-1620916297754-0a2c2e59b76b?w=400&q=80',
            'Glow Recipe Watermelon Sleeping Mask': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&q=80',
        }

        updated_count = 0
        for product_name, image_url in product_images.items():
            try:
                product = Product.objects.get(name=product_name)
                # Save the image URL directly in a custom field or update product
                # For now, we'll just mark that it should use this URL
                self.stdout.write(f"✓ Image URL for: {product.brand} - {product.name}")
                self.stdout.write(f"  URL: {image_url}")
                updated_count += 1
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"✗ Product not found: {product_name}"))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Mapped {updated_count} product images!'))
        self.stdout.write(self.style.WARNING('\nNote: Images are displayed as gradient placeholders by default.'))
        self.stdout.write('To use actual images, you can:')
        self.stdout.write('1. Upload images through Django Admin')
        self.stdout.write('2. Download images and add them to media folder')
        self.stdout.write('3. Use the URLs above with an image proxy service')
