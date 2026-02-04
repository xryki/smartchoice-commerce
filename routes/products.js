const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

// Obtenir tous les produits
router.get('/', async (req, res) => {
    try {
        const products = await Product.find({ inStock: true });
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
        const products = await Product.find({ featured: true, inStock: true })
            .sort({ rating: -1, reviewCount: -1 })
            .limit(8);
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
        
        let searchQuery = { inStock: true };
        
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
            
            searchQuery.$or = [
                { name: { $regex: searchTerms.join('|'), $options: 'i' } },
                { brand: { $regex: searchTerms.join('|'), $options: 'i' } },
                { description: { $regex: searchTerms.join('|'), $options: 'i' } }
            ];
        }
        
        if (category) searchQuery.category = category;
        if (brand) searchQuery.brand = brand;
        if (minPrice) searchQuery.price = { $gte: minPrice };
        if (maxPrice) searchQuery.price = { ...searchQuery.price, $lte: maxPrice };
        
        // Tri
        let sortOptions = {};
        switch (sortBy) {
            case 'price_low':
                sortOptions = { price: 1 };
                break;
            case 'price_high':
                sortOptions = { price: -1 };
                break;
            case 'rating':
                sortOptions = { rating: -1 };
                break;
            case 'newest':
                sortOptions = { createdAt: -1 };
                break;
            case 'discount':
                sortOptions = { discountPercentage: -1 };
                break;
            default: // relevance
                sortOptions = { featured: -1, rating: -1, reviewCount: -1 };
        }
        
        const products = await Product.find(searchQuery)
            .sort(sortOptions)
            .limit(50);
        
        res.json({
            products,
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
        const categories = await Product.distinct('category', { inStock: true });
        res.json({ categories: categories.sort() });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des catégories' });
    }
});

// Obtenir les marques
router.get('/brands', async (req, res) => {
    try {
        const { category } = req.query;
        const query = category ? { category, inStock: true } : { inStock: true };
        const brands = await Product.distinct('brand', query);
        res.json({ brands: brands.sort() });
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de la récupération des marques' });
    }
});

module.exports = router;
