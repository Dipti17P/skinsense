import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skinsense.settings')
django.setup()

from products.models import Product

print('\n📦 Products by Skin Type:')
print('=' * 40)
for skin_type in ['dry', 'oily', 'combination', 'sensitive', 'normal']:
    count = Product.objects.filter(skin_type=skin_type).count()
    print(f'{skin_type.title():12}: {count} products')

print('=' * 40)
print(f'Total: {Product.objects.count()} products')
