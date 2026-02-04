const express = require('express');
const router = express.Router();
const multer = require('multer');
const { productsData } = require('../data/products');

// Configuration de multer pour l'upload d'images
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Identification d'objet depuis une image
router.post('/identify', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Aucune image fournie' });
        }
        
        // Analyse basique de l'image (simulation)
        const detection = analyzeImage(req.file.originalname);
        
        // Recherche de produits similaires
        const similarProducts = await findSimilarProducts(detection);
        
        res.json({
            success: true,
            detection,
            similarProducts,
            totalProducts: similarProducts.length
        });
        
    } catch (error) {
        console.error('Erreur vision:', error);
        res.status(500).json({ error: 'Erreur lors de l\'analyse de l\'image' });
    }
});

// Analyse basique d'image basée sur le nom du fichier
function analyzeImage(filename) {
    const filenameLower = filename.toLowerCase();
    
    // Mapping des objets
    const objectMapping = {
        'iphone': { object: 'smartphone', keywords: ['telephone', 'apple', 'iphone'] },
        'samsung': { object: 'smartphone', keywords: ['telephone', 'samsung', 'galaxy'] },
        'macbook': { object: 'laptop', keywords: ['ordinateur', 'portable', 'apple'] },
        'playstation': { object: 'console', keywords: ['console', 'sony', 'ps5'] },
        'xbox': { object: 'console', keywords: ['console', 'microsoft', 'xbox'] },
        'watch': { object: 'montre', keywords: ['montre', 'apple watch'] },
        'camera': { object: 'camera', keywords: ['appareil photo', 'gopro'] },
        'headphone': { object: 'casque', keywords: ['casque', 'audio', 'sony'] },
        'mouse': { object: 'souris', keywords: ['souris', 'logitech'] },
        'keyboard': { object: 'clavier', keywords: ['clavier', 'logitech'] },
        'monitor': { object: 'ecran', keywords: ['ecran', 'samsung'] },
        'tv': { object: 'television', keywords: ['television', 'ecran'] },
        'laptop': { object: 'ordinateur', keywords: ['ordinateur', 'portable'] },
        'computer': { object: 'ordinateur', keywords: ['ordinateur', 'pc'] },
        'gpu': { object: 'carte graphique', keywords: ['carte graphique', 'nvidia'] },
        'cpu': { object: 'processeur', keywords: ['processeur', 'amd'] }
    };
    
    for (const [key, value] of Object.entries(objectMapping)) {
        if (filenameLower.includes(key)) {
            return {
                ...value,
                confidence: 0.8,
                source: 'filename_analysis'
            };
        }
    }
    
    // Par défaut
    return {
        object: 'objet electronique',
        keywords: ['electronique', 'produit'],
        confidence: 0.5,
        source: 'default'
    };
}

// Recherche de produits similaires
async function findSimilarProducts(detection) {
    try {
        const keywords = detection.keywords;
        let allProducts = [];
        
        // Rechercher pour chaque mot-clé
        for (const keyword of keywords) {
            const products = productsData.filter(product => {
                return product.name.toLowerCase().includes(keyword) ||
                       product.brand.toLowerCase().includes(keyword) ||
                       (product.description && product.description.toLowerCase().includes(keyword));
            });
            allProducts = allProducts.concat(products);
        }
        
        // Éliminer les doublons
        const uniqueProducts = [];
        const seenNames = new Set();
        
        for (const product of allProducts) {
            if (!seenNames.has(product.name)) {
                uniqueProducts.push(product);
                seenNames.add(product.name);
            }
        }
        
        // Trier par pertinence
        uniqueProducts.sort((a, b) => {
            if (a.featured && !b.featured) return -1;
            if (!a.featured && b.featured) return 1;
            if (a.rating !== b.rating) return b.rating - a.rating;
            return b.reviewCount - a.reviewCount;
        });
        
        return uniqueProducts.filter(p => p.inStock).slice(0, 12);
        
    } catch (error) {
        console.error('Erreur recherche produits:', error);
        return [];
    }
}

module.exports = router;
