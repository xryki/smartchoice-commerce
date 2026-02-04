# Part 1: Apple, Samsung, Sony, Google, Microsoft

real_products_part1 = [
    # Apple Products
    {
        'name': 'Apple Watch Series 10 GPS 45mm',
        'category': 'electronics',
        'brand': 'Apple',
        'price': 549.99,
        'original_price': 599.99,
        'discount_percentage': 8,
        'rating': 4.7,
        'review_count': 2453,
        'quality_score': 95,
        'description': 'Nouvelle Apple Watch Series 10 avec écran plus grand, capteurs santé avancés et autonomie améliorée.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B0DG7YJ4X2',
        'fnac_url': 'https://www.fnac.com/Apple-Watch-Series-10-GPS-45mm/a17061441',
        'darty_url': 'https://www.darty.com/product/informatique/montre-connectee/apple/apple-watch-series-10-gps-45mm/89041521.html',
        'featured': True,
        'in_stock': True
    },
    {
        'name': 'iPhone 15 Pro Max 256GB Titane Naturel',
        'category': 'electronics',
        'brand': 'Apple',
        'price': 1289.99,
        'original_price': 1449.99,
        'discount_percentage': 11,
        'rating': 4.8,
        'review_count': 5234,
        'quality_score': 98,
        'description': 'iPhone 15 Pro Max avec puce A17 Pro, système photo avancé et design en titane.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B0CHX2XQ2F',
        'fnac_url': 'https://www.fnac.com/iPhone-15-Pro-Max-256-GP-Titane-Naturel/a17061442',
        'darty_url': 'https://www.darty.com/product/informatique/smartphone/apple/iphone-15-pro-max-256gb-titane-naturel/89041522.html',
        'featured': True,
        'in_stock': True
    },
    
    # Samsung Products
    {
        'name': 'Samsung Galaxy S24 Ultra 256GB Titanium Black',
        'category': 'electronics',
        'brand': 'Samsung',
        'price': 1199.99,
        'original_price': 1399.99,
        'discount_percentage': 14,
        'rating': 4.7,
        'review_count': 4532,
        'quality_score': 93,
        'description': 'Samsung Galaxy S24 Ultra avec écran Dynamic AMOLED 2X, S Pen et caméra 200MP.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B0CHX2YQ4H',
        'fnac_url': 'https://www.fnac.com/Samsung-Galaxy-S24-Ultra-256GB-Titanium-Black/a17061446',
        'darty_url': 'https://www.darty.com/product/informatique/smartphone/samsung/samsung-galaxy-s24-ultra-256gb-titanium-black/89041526.html',
        'featured': True,
        'in_stock': True
    },
    {
        'name': 'Samsung Odyssey G9 49" 240Hz Curved Gaming Monitor',
        'category': 'electronics',
        'brand': 'Samsung',
        'price': 1299.99,
        'original_price': 1599.99,
        'discount_percentage': 19,
        'rating': 4.7,
        'review_count': 1834,
        'quality_score': 92,
        'description': 'Moniteur gaming incurvé 49 pouces, 240Hz, QLED, HDR1000 et résolution Dual QHD.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B08H93YK2V',
        'fnac_url': 'https://www.fnac.com/Samsung-Odyssey-G9-49-240Hz-Curved-Gaming-Monitor/a17061446',
        'darty_url': 'https://www.darty.com/product/informatique/moniteur-pc/samsung/samsung-odyssey-g9-49-240hz-curved-gaming-monitor/89041524.html',
        'featured': True,
        'in_stock': True
    },
    
    # Sony Products
    {
        'name': 'PlayStation 5 Slim Console Edition Standard',
        'category': 'electronics',
        'brand': 'Sony',
        'price': 449.99,
        'original_price': 549.99,
        'discount_percentage': 18,
        'rating': 4.8,
        'review_count': 8765,
        'quality_score': 95,
        'description': 'Console PlayStation 5 Slim avec lecteur Blu-ray, manette DualSense et 1 To de stockage.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B0CHL2XQ5H',
        'fnac_url': 'https://www.fnac.com/PlayStation-5-Slim-Console-Edition-Standard/a17061447',
        'darty_url': 'https://www.darty.com/product/informatique/console-de-jeux/sony/playstation-5-slim-console-edition-standard/89041525.html',
        'featured': True,
        'in_stock': True
    },
    
    # Google Products
    {
        'name': 'Google Pixel 8 Pro 256GB Porcelain',
        'category': 'electronics',
        'brand': 'Google',
        'price': 999.99,
        'original_price': 1099.99,
        'discount_percentage': 9,
        'rating': 4.6,
        'review_count': 4321,
        'quality_score': 91,
        'description': 'Google Pixel 8 Pro avec écran 6.7 pouces, processeur Tensor G3 et caméra 50MP.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B0CHX2YQ4L',
        'fnac_url': 'https://www.fnac.com/Google-Pixel-8-Pro-256GB-Porcelain/a17061452',
        'darty_url': 'https://www.darty.com/product/informatique/smartphone/google/google-pixel-8-pro-256gb-porcelain/89041532.html',
        'featured': True,
        'in_stock': True
    },
    
    # Microsoft Products
    {
        'name': 'Xbox Series X 1TB SSD',
        'category': 'electronics',
        'brand': 'Microsoft',
        'price': 449.99,
        'original_price': 549.99,
        'discount_percentage': 18,
        'rating': 4.7,
        'review_count': 6543,
        'quality_score': 93,
        'description': 'Console Xbox Series X avec SSD 1To, manette sans fil et Game Pass.',
        'image_url': 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        'amazon_url': 'https://www.amazon.fr/dp/B08H93YK2P',
        'fnac_url': 'https://www.fnac.com/Xbox-Series-X-1TB-SSD/a17061455',
        'darty_url': 'https://www.darty.com/product/informatique/console-de-jeux/microsoft/xbox-series-x-1tb-ssd/89041535.html',
        'featured': True,
        'in_stock': True
    }
]
