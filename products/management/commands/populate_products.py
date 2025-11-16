from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Populate the database with sample skincare products'

    def handle(self, *args, **kwargs):
        products_data = [
            # DRY SKIN PRODUCTS
            {
                'name': 'Hydrating Facial Cleanser',
                'brand': 'CeraVe',
                'product_type': 'Cleanser',
                'skin_type': 'dry',
                'description': 'Gentle, non-foaming cleanser with hyaluronic acid and ceramides to hydrate and restore the skin barrier.',
                'link': 'https://www.cerave.com/skincare/cleansers/hydrating-facial-cleanser',
            },
            {
                'name': 'Ultra Facial Cream',
                'brand': "Kiehl's",
                'product_type': 'Moisturizer',
                'skin_type': 'dry',
                'description': '24-hour hydration with glacial glycoprotein and desert plant extracts. Lightweight yet deeply moisturizing.',
                'link': 'https://www.kiehls.com/skincare/face-moisturizers/ultra-facial-cream/622.html',
            },
            {
                'name': 'Toleriane Double Repair Face Moisturizer',
                'brand': 'La Roche-Posay',
                'product_type': 'Moisturizer',
                'skin_type': 'dry',
                'description': 'Prebiotic thermal water moisturizer with ceramides and niacinamide for intense hydration.',
                'link': 'https://www.laroche-posay.us/our-products/face/face-moisturizer/toleriane-double-repair-face-moisturizer-3337875545846.html',
            },
            {
                'name': 'Midnight Recovery Concentrate',
                'brand': "Kiehl's",
                'product_type': 'Serum',
                'skin_type': 'dry',
                'description': 'Essential oils blend that helps skin recover overnight. Replenishes and restores radiance.',
                'link': 'https://www.kiehls.com/skincare/face-serums/midnight-recovery-concentrate/799.html',
            },
            
            # OILY SKIN PRODUCTS
            {
                'name': 'Foaming Facial Cleanser',
                'brand': 'CeraVe',
                'product_type': 'Cleanser',
                'skin_type': 'oily',
                'description': 'Refreshing foam formula with ceramides and niacinamide. Removes excess oil without stripping skin.',
                'link': 'https://www.cerave.com/skincare/cleansers/foaming-facial-cleanser',
            },
            {
                'name': 'Effaclar Duo Dual Action Acne Treatment',
                'brand': 'La Roche-Posay',
                'product_type': 'Treatment',
                'skin_type': 'oily',
                'description': 'Targets acne, unclogs pores, and reduces excess oil. Contains benzoyl peroxide and micro-exfoliating LHA.',
                'link': 'https://www.laroche-posay.us/our-products/face/face-moisturizer/effaclar-duo-dual-acne-treatment-3337875545839.html',
            },
            {
                'name': 'Oil-Free Acne Moisturizer',
                'brand': 'Neutrogena',
                'product_type': 'Moisturizer',
                'skin_type': 'oily',
                'description': 'Lightweight, pink grapefruit moisturizer with salicylic acid to treat and prevent breakouts.',
                'link': 'https://www.neutrogena.com/products/skincare/oil-free-acne-moisturizer-pink-grapefruit/6811047.html',
            },
            {
                'name': 'Niacinamide 10% + Zinc 1%',
                'brand': 'The Ordinary',
                'product_type': 'Serum',
                'skin_type': 'oily',
                'description': 'High-strength vitamin and mineral formula to reduce blemishes and balance oil production.',
                'link': 'https://theordinary.com/en-us/niacinamide-10-zinc-1-serum-100411.html',
            },
            {
                'name': 'Supermud Clearing Treatment',
                'brand': 'GlamGlow',
                'product_type': 'Mask',
                'skin_type': 'oily',
                'description': 'Activated charcoal mask that draws out impurities and clears pores for clearer skin.',
                'link': 'https://www.glamglow.com/product/19116/59944/masks/supermud/clearing-treatment',
            },
            
            # COMBINATION SKIN PRODUCTS
            {
                'name': 'Dramatically Different Moisturizing Gel',
                'brand': 'Clinique',
                'product_type': 'Moisturizer',
                'skin_type': 'combination',
                'description': 'Oil-free gel that hydrates and balances combination skin without adding shine.',
                'link': 'https://www.clinique.com/product/1687/5047/skin-care/moisturizers/dramatically-different-moisturizing-gel',
            },
            {
                'name': 'Daily Microfoliant',
                'brand': 'Dermalogica',
                'product_type': 'Exfoliator',
                'skin_type': 'combination',
                'description': 'Rice-based powder exfoliant that activates with water. Gently buffs away dead skin cells.',
                'link': 'https://www.dermalogica.com/products/daily-microfoliant',
            },
            {
                'name': 'Hydro Boost Water Gel',
                'brand': 'Neutrogena',
                'product_type': 'Moisturizer',
                'skin_type': 'combination',
                'description': 'Oil-free gel-cream with hyaluronic acid. Absorbs quickly for long-lasting hydration.',
                'link': 'https://www.neutrogena.com/products/skincare/hydro-boost-water-gel-with-hyaluronic-acid/6811048.html',
            },
            {
                'name': 'Multi-Active Day Cream',
                'brand': 'Clarins',
                'product_type': 'Day Cream',
                'skin_type': 'combination',
                'description': 'Lightweight day cream that targets first signs of aging while balancing skin.',
                'link': 'https://www.clarins.com/multi-active-day-cream-all-skin-types/80056966.html',
            },
            
            # SENSITIVE SKIN PRODUCTS
            {
                'name': 'Ultra Gentle Hydrating Cleanser',
                'brand': 'First Aid Beauty',
                'product_type': 'Cleanser',
                'skin_type': 'sensitive',
                'description': 'Soap-free, pH-balanced cleanser that gently removes makeup and impurities without irritation.',
                'link': 'https://www.firstaidbeauty.com/skin-care-products/cleansers-exfoliators/face-cleanser',
            },
            {
                'name': 'Cicaplast Baume B5',
                'brand': 'La Roche-Posay',
                'product_type': 'Balm',
                'skin_type': 'sensitive',
                'description': 'Multi-purpose soothing balm with panthenol and madecassoside to repair and protect irritated skin.',
                'link': 'https://www.laroche-posay.us/our-products/face/face-moisturizer/cicaplast-baume-b5-for-dry-skin-irritations-3337875545815.html',
            },
            {
                'name': 'Skin Recovery Cream',
                'brand': "Paula's Choice",
                'product_type': 'Moisturizer',
                'skin_type': 'sensitive',
                'description': 'Rich, calming cream with plant extracts and antioxidants for very dry, sensitive skin.',
                'link': 'https://www.paulaschoice.com/skin-recovery-enriched-calming-toner/126.html',
            },
            {
                'name': 'Redness Relief SPF 30',
                'brand': 'Aveeno',
                'product_type': 'Sunscreen',
                'skin_type': 'sensitive',
                'description': 'Mineral sunscreen with feverfew to calm and protect sensitive, redness-prone skin.',
                'link': 'https://www.aveeno.com/products/ultra-calming-daily-moisturizer-broad-spectrum-spf-30',
            },
            
            # NORMAL SKIN PRODUCTS
            {
                'name': 'Take The Day Off Cleansing Balm',
                'brand': 'Clinique',
                'product_type': 'Cleanser',
                'skin_type': 'normal',
                'description': 'Luxurious balm melts away makeup and impurities. Leaves skin soft and radiant.',
                'link': 'https://www.clinique.com/product/1683/6424/skin-care/cleansers-makeup-removers/take-the-day-off-cleansing-balm',
            },
            {
                'name': 'Moisture Surge 100H Auto-Replenishing Hydrator',
                'brand': 'Clinique',
                'product_type': 'Moisturizer',
                'skin_type': 'normal',
                'description': 'Oil-free gel-cream provides 100 hours of hydration with aloe bioferment and hyaluronic acid.',
                'link': 'https://www.clinique.com/product/1687/38893/skin-care/moisturizers/moisture-surge-100h-auto-replenishing-hydrator',
            },
            {
                'name': 'Vitamin C Serum',
                'brand': 'TruSkin',
                'product_type': 'Serum',
                'skin_type': 'normal',
                'description': 'Brightening serum with vitamin C, hyaluronic acid, and vitamin E for radiant, youthful skin.',
                'link': 'https://www.truskin.com/products/vitamin-c-serum',
            },
            {
                'name': 'Advanced Night Repair',
                'brand': 'Estée Lauder',
                'product_type': 'Night Serum',
                'skin_type': 'normal',
                'description': 'Iconic night serum that repairs and renews skin while you sleep. Reduces visible signs of aging.',
                'link': 'https://www.esteelauder.com/product/681/22788/product-catalog/skincare/advanced-night-repair',
            },
            {
                'name': 'Glow Recipe Watermelon Sleeping Mask',
                'brand': 'Glow Recipe',
                'product_type': 'Mask',
                'skin_type': 'normal',
                'description': 'Bouncy overnight mask with watermelon and hyaluronic acid for a refreshed, glowing complexion.',
                'link': 'https://www.glowrecipe.com/products/watermelon-glow-sleeping-mask',
            },
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                brand=product_data['brand'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"✓ Created: {product.brand} - {product.name}")
            else:
                self.stdout.write(self.style.WARNING(f"○ Skipped (exists): {product.brand} - {product.name}"))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {created_count} new products!'))
        self.stdout.write(f'Total products in database: {Product.objects.count()}')
