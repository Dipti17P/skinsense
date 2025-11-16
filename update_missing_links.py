import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skinsense.settings')
django.setup()

from products.models import Product

# Update products without links
updates = [
    {'brand': 'CeraVe', 'name': 'Hydrating Moisturizer', 'link': 'https://www.flipkart.com/search?q=cerave+hydrating+moisturizer'},
    {'brand': 'Neutrogena', 'name': 'Oil Control Gel', 'link': 'https://www.flipkart.com/search?q=neutrogena+oil+control+gel'},
    {'brand': 'Simple', 'name': 'Gentle Cleanser', 'link': 'https://www.flipkart.com/search?q=simple+gentle+cleanser'},
]

for update in updates:
    try:
        product = Product.objects.get(brand=update['brand'], name=update['name'])
        product.link = update['link']
        product.save()
        print(f"✓ Updated: {product.brand} - {product.name}")
    except Product.DoesNotExist:
        print(f"✗ Not found: {update['brand']} - {update['name']}")

print('\n✅ All products updated with Flipkart links!')
