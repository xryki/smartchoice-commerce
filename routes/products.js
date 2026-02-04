const express = require('express');
const router = express.Router();
const { productsData } = require('../data/products');

// Obtenir tous les produits
router.get('/', async (req, res) => {
    try {
        const products = productsData.filter(p => p.inStock);
        res.json({
            products,
            total: products.length
        });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des produits' });
    }
});

// Obtenir les produits vedettes
router.get('/featured', async (req, res) => {
    try {
        const products = productsData
            .filter(p => p.featured && p.inStock)
            .sort((a, b) => b.rating - a.rating)
            .slice(0, 8);
        res.json({
            products,
            total: products.length
        });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des produits vedettes' });
    }
});

// Recherche avancée
router.post('/search', async (req, res) => {
    try {
        const { query, category, brand, minPrice, maxPrice, sortBy = 'relevance' } = req.body;
        
        let products = productsData.filter(p => p.inStock);
        
        // Recherche par mots-clés intelligente
        if (query) {
            const queryLower = query.toLowerCase();
            
            // Mapping des mots-clés
            const keywordMap = {
                'montre': ['apple watch', 'watch'],
                'telephone': ['iphone', 'phone', 'smartphone', 'samsung'],
                'portable': ['iphone', 'phone', 'smartphone'],
                'ordinateur': ['macbook', 'laptop', 'computer', 'asus', 'hp'],
                'pc': ['computer', 'desktop'],
                'carte graphique': ['rtx', 'nvidia', 'gpu'],
                'gpu': ['rtx', 'nvidia', 'graphics'],
                'processeur': ['amd', 'ryzen', 'cpu'],
                'cpu': ['amd', 'ryzen', 'processor'],
                'ecran': ['samsung', 'odyssey', 'monitor'],
                'console': ['playstation', 'ps5', 'sony'],
                'souris': ['logitech', 'mouse'],
                'apple': ['apple', 'iphone', 'macbook', 'apple watch'],
                'samsung': ['samsung', 'odyssey'],
                'sony': ['sony', 'playstation', 'ps5'],
                'nvidia': ['nvidia', 'rtx'],
                'amd': ['amd', 'ryzen'],
                'logitech': ['logitech', 'mouse'],
                'gaming': ['playstation', 'ps5', 'rtx'],
                'jeux': ['playstation', 'ps5', 'gaming']
            };
            
            // Construire la recherche
            const searchTerms = [queryLower];
            for (const [key, related] of Object.entries(keywordMap)) {
                if (key.includes(queryLower)) {
                    searchTerms.push(...related);
                }
            }
            
            products = products.filter(product => {
                return searchTerms.some(term => 
                    product.name.toLowerCase().includes(term) ||
                    product.brand.toLowerCase().includes(term) ||
                    (product.description && product.description.toLowerCase().includes(term))
                );
            });
        }
        
        if (category) products = products.filter(p => p.category === category);
        if (brand) products = products.filter(p => p.brand === brand);
        if (minPrice) products = products.filter(p => p.price >= minPrice);
        if (maxPrice) products = products.filter(p => p.price <= maxPrice);
        
        // Tri
        switch (sortBy) {
            case 'price_low':
                products.sort((a, b) => a.price - b.price);
                break;
            case 'price_high':
                products.sort((a, b) => b.price - a.price);
                break;
            case 'rating':
                products.sort((a, b) => b.rating - a.rating);
                break;
            case 'newest':
                products.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
                break;
            case 'discount':
                products.sort((a, b) => b.discountPercentage - a.discountPercentage);
                break;
            default: // relevance
                products.sort((a, b) => {
                    if (a.featured && !b.featured) return -1;
                    if (!a.featured && b.featured) return 1;
                    if (a.rating !== b.rating) return b.rating - a.rating;
                    return b.reviewCount - a.reviewCount;
                });
        }
        
        res.json({
            products: products.slice(0, 50),
            total: products.length,
            query
        });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la recherche' });
    }
});

// Obtenir les catégories
router.get('/categories', async (req, res) => {
    try {
        const categories = [...new Set(productsData.filter(p => p.inStock).map(p => p.category))];
        res.json({ categories: categories.sort() });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des catégories' });
    }
});

// Obtenir les marques
router.get('/brands', async (req, res) => {
    try {
        const { category } = req.query;
        let products = productsData.filter(p => p.inStock);
        if (category) products = products.filter(p => p.category === category);
        const brands = [...new Set(products.map(p => p.brand))];
        res.json({ brands: brands.sort() });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des marques' });
    }
});

module.exports = router;
