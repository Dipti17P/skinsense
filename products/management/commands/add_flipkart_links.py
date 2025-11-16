from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update products with Flipkart links'

    def handle(self, *args, **kwargs):
        # Flipkart links for products (search URLs for each product)
        flipkart_links = {
            'Hydrating Facial Cleanser': 'https://www.flipkart.com/search?q=cerave+hydrating+facial+cleanser',
            'Ultra Facial Cream': 'https://www.flipkart.com/search?q=kiehls+ultra+facial+cream',
            'Toleriane Double Repair Face Moisturizer': 'https://www.flipkart.com/search?q=la+roche+posay+toleriane+double+repair',
            'Midnight Recovery Concentrate': 'https://www.flipkart.com/search?q=kiehls+midnight+recovery+concentrate',
            'Foaming Facial Cleanser': 'https://www.flipkart.com/search?q=cerave+foaming+facial+cleanser',
            'Effaclar Duo Dual Action Acne Treatment': 'https://www.flipkart.com/search?q=la+roche+posay+effaclar+duo',
            'Oil-Free Acne Moisturizer': 'https://www.flipkart.com/search?q=neutrogena+oil+free+acne+moisturizer',
            'Niacinamide 10% + Zinc 1%': 'https://www.flipkart.com/search?q=the+ordinary+niacinamide+10+zinc+1',
            'Supermud Clearing Treatment': 'https://www.flipkart.com/search?q=glamglow+supermud+clearing+treatment',
            'Dramatically Different Moisturizing Gel': 'https://www.flipkart.com/search?q=clinique+dramatically+different+moisturizing+gel',
            'Daily Microfoliant': 'https://www.flipkart.com/search?q=dermalogica+daily+microfoliant',
            'Hydro Boost Water Gel': 'https://www.flipkart.com/search?q=neutrogena+hydro+boost+water+gel',
            'Multi-Active Day Cream': 'https://www.flipkart.com/search?q=clarins+multi+active+day+cream',
            'Ultra Gentle Hydrating Cleanser': 'https://www.flipkart.com/search?q=first+aid+beauty+ultra+gentle+cleanser',
            'Cicaplast Baume B5': 'https://www.flipkart.com/search?q=la+roche+posay+cicaplast+baume+b5',
            'Skin Recovery Cream': 'https://www.flipkart.com/search?q=paulas+choice+skin+recovery+cream',
            'Redness Relief SPF 30': 'https://www.flipkart.com/search?q=aveeno+redness+relief+spf+30',
            'Take The Day Off Cleansing Balm': 'https://www.flipkart.com/search?q=clinique+take+the+day+off+cleansing+balm',
            'Moisture Surge 100H Auto-Replenishing Hydrator': 'https://www.flipkart.com/search?q=clinique+moisture+surge+100h',
            'Vitamin C Serum': 'https://www.flipkart.com/search?q=truskin+vitamin+c+serum',
            'Advanced Night Repair': 'https://www.flipkart.com/search?q=estee+lauder+advanced+night+repair',
            'Glow Recipe Watermelon Sleeping Mask': 'https://www.flipkart.com/search?q=glow+recipe+watermelon+sleeping+mask',
        }

        updated_count = 0
        for product_name, flipkart_url in flipkart_links.items():
            try:
                product = Product.objects.get(name=product_name)
                product.link = flipkart_url
                product.save()
                updated_count += 1
                self.stdout.write(f"✓ Updated: {product.brand} - {product.name}")
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"✗ Product not found: {product_name}"))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully updated {updated_count} products with Flipkart links!'))
