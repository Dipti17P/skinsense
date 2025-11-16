import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skinsense.settings')
django.setup()

from products.models import Product

print('\n🔗 Products with Flipkart Links:')
print('=' * 60)

products_with_links = Product.objects.exclude(link__isnull=True).exclude(link='')
products_without_links = Product.objects.filter(link__isnull=True) | Product.objects.filter(link='')

print(f'\n✅ Products WITH Flipkart links: {products_with_links.count()}')
for p in products_with_links[:5]:
    print(f'  • {p.brand} - {p.name}')
    print(f'    Link: {p.link[:60]}...')

print(f'\n❌ Products WITHOUT links: {products_without_links.count()}')
for p in products_without_links[:5]:
    print(f'  • {p.brand} - {p.name}')

print('=' * 60)
