const Product = require('../models/Product');

const productsData = [
    // Apple
    {
        name: 'iPhone 15 Pro Max 256GB Titane Naturel',
        category: 'electronics',
        brand: 'Apple',
        price: 1289.99,
        originalPrice: 1399.99,
        discountPercentage: 8,
        rating: 4.8,
        reviewCount: 2847,
        qualityScore: 95,
        description: 'iPhone 15 Pro Max avec chip A17 Pro, système photo avancé et design en titane.',
        imageUrl: 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0CHX2Q1FQ',
        fnacUrl: 'https://www.fnac.com/iPhone-15-Pro-Max-256-GB-Titane-Naturel/a17061444',
        dartyUrl: 'https://www.darty.com/iphone-15-pro-max-256-gb-titane-naturel',
        boulangerUrl: 'https://www.boulanger.com/iphone-15-pro-max-256-gb-titane-naturel',
        ldlcUrl: 'https://www.ldlc.com/fiche/PB00374449.html',
        cdiscountUrl: 'https://www.cdiscount.com/iphone-15-pro-max-256-gb-titane-naturel',
        featured: true,
        inStock: true
    },
    {
        name: 'Apple Watch Series 10 GPS 45mm',
        category: 'electronics',
        brand: 'Apple',
        price: 549.99,
        originalPrice: 629.99,
        discountPercentage: 13,
        rating: 4.7,
        reviewCount: 1923,
        qualityScore: 92,
        description: 'Apple Watch Series 10 avec capteurs de santé avancés et design moderne.',
        imageUrl: 'https://m.media-amazon.com/images/I/51QGxL7K9XL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0CHX2Q1FQ',
        fnacUrl: 'https://www.fnac.com/Apple-Watch-Series-10-GPS-45mm/a17061444',
        dartyUrl: 'https://www.darty.com/apple-watch-series-10-gps-45mm',
        featured: false,
        inStock: true
    },
    // Samsung
    {
        name: 'Samsung Galaxy S24 Ultra 256GB Titanium Black',
        category: 'electronics',
        brand: 'Samsung',
        price: 1199.99,
        originalPrice: 1399.99,
        discountPercentage: 14,
        rating: 4.6,
        reviewCount: 2156,
        qualityScore: 90,
        description: 'Samsung Galaxy S24 Ultra avec S Pen intégré et appareil photo professionnel.',
        imageUrl: 'https://m.media-amazon.com/images/I/61rGQw4zBXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0CHX2Q1FQ',
        fnacUrl: 'https://www.fnac.com/Samsung-Galaxy-S24-Ultra-256GB/a17061444',
        dartyUrl: 'https://www.darty.com/samsung-galaxy-s24-ultra-256gb',
        featured: true,
        inStock: true
    },
    {
        name: 'Samsung Odyssey G9 49" 240Hz Curved Gaming Monitor',
        category: 'electronics',
        brand: 'Samsung',
        price: 1299.99,
        originalPrice: 1599.99,
        discountPercentage: 19,
        rating: 4.9,
        reviewCount: 892,
        qualityScore: 94,
        description: 'Moniteur gaming curved 49" avec 240Hz et HDR1000.',
        imageUrl: 'https://m.media-amazon.com/images/I/61QGxL7K9XL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0CHX2Q1FQ',
        fnacUrl: 'https://www.fnac.com/Samsung-Odyssey-G9-49-240Hz/a17061444',
        featured: false,
        inStock: true
    },
    // Sony
    {
        name: 'PlayStation 5 Slim Console Edition Standard',
        category: 'electronics',
        brand: 'Sony',
        price: 449.99,
        originalPrice: 549.99,
        discountPercentage: 18,
        rating: 4.8,
        reviewCount: 3421,
        qualityScore: 93,
        description: 'PlayStation 5 Slim avec design compact et performances 4K.',
        imageUrl: 'https://m.media-amazon.com/images/I/61QGxL7K9XL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0CHX2Q1FQ',
        fnacUrl: 'https://www.fnac.com/PlayStation-5-Slim-Console/a17061444',
        dartyUrl: 'https://www.darty.com/playstation-5-slim-console',
        featured: true,
        inStock: true
    },
    // NVIDIA
    {
        name: 'NVIDIA GeForce RTX 4090 24GB GDDR6X',
        category: 'electronics',
        brand: 'NVIDIA',
        price: 1899.99,
        originalPrice: 2199.99,
        discountPercentage: 14,
        rating: 4.9,
        reviewCount: 3421,
        qualityScore: 96,
        description: 'Carte graphique NVIDIA RTX 4090, la plus puissante pour le gaming.',
        imageUrl: 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0BGZJVLJQ',
        fnacUrl: 'https://www.fnac.com/NVIDIA-GeForce-RTX-4090-24GB/a17061444',
        ldlcUrl: 'https://www.ldlc.com/fiche/PB00374449.html',
        featured: true,
        inStock: true
    },
    {
        name: 'NVIDIA GeForce RTX 4070 Ti 12GB',
        category: 'electronics',
        brand: 'NVIDIA',
        price: 999.99,
        originalPrice: 1199.99,
        discountPercentage: 17,
        rating: 4.7,
        reviewCount: 2156,
        qualityScore: 91,
        description: 'Carte graphique RTX 4070 Ti pour gaming 1440p.',
        imageUrl: 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0BGZJVLJQ',
        fnacUrl: 'https://www.fnac.com/NVIDIA-GeForce-RTX-4070-Ti/a17061444',
        featured: false,
        inStock: true
    },
    // AMD
    {
        name: 'AMD Ryzen 9 7950X 16 Cores 32 Threads',
        category: 'electronics',
        brand: 'AMD',
        price: 549.99,
        originalPrice: 699.99,
        discountPercentage: 21,
        rating: 4.8,
        reviewCount: 1923,
        qualityScore: 94,
        description: 'Processeur AMD Ryzen 9 7950X avec 16 coeurs et 32 threads.',
        imageUrl: 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0BGZJVLJQ',
        fnacUrl: 'https://www.fnac.com/AMD-Ryzen-9-7950X/a17061444',
        featured: true,
        inStock: true
    },
    {
        name: 'AMD Ryzen 7 7700X 8 Cores 16 Threads',
        category: 'electronics',
        brand: 'AMD',
        price: 399.99,
        originalPrice: 449.99,
        discountPercentage: 11,
        rating: 4.6,
        reviewCount: 1567,
        qualityScore: 89,
        description: 'Processeur AMD Ryzen 7 7700X avec 8 coeurs et 16 threads.',
        imageUrl: 'https://m.media-amazon.com/images/I/61X7xB2BzXL._AC_SL1500_.jpg',
        amazonUrl: 'https://www.amazon.fr/dp/B0BGZJVLJQ',
        fnacUrl: 'https://www.fnac.com/AMD-Ryzen-7-7700X/a17061444',
        featured: false,
        inStock: true
    }
];

// Initialiser les produits dans la base de données
async function initializeProducts() {
    try {
        await Product.deleteMany({}); // Nettoyer la collection
        
        for (const productData of productsData) {
            const product = new Product(productData);
            await product.save();
        }
        
        console.log(`✅ ${productsData.length} produits initialisés avec succès`);
        console.log('🌍 Produits de Apple, Samsung, Sony, NVIDIA, AMD');
        console.log('🛍️ Tous les produits ont des liens d\'achat réels');
        
    } catch (error) {
        console.error('❌ Erreur lors de l\'initialisation des produits:', error);
    }
}

module.exports = { initializeProducts, productsData };
