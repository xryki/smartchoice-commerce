const express = require('express');
const router = express.Router();
const multer = require('multer');
const sharp = require('sharp');
const Product = require('../models/Product');

// Configuration de multer pour l'upload d'images
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Identification d'objet depuis une image
router.post('/identify', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Aucune image fournie' });
        }
        
        // Traitement de l'image avec sharp
        const processedImage = await sharp(req.file.buffer)
            .resize(800, 800, { fit: 'inside' })
            .jpeg({ quality: 80 })
            .toBuffer();
        
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
            const products = await Product.find({
                $or: [
                    { name: { $regex: keyword, $options: 'i' } },
                    { brand: { $regex: keyword, $options: 'i' } },
                    { description: { $regex: keyword, $options: 'i' } }
                ],
                inStock: true
            });
            allProducts = allProducts.concat(products);
        }
        
        // Éliminer les doublons
        const uniqueProducts = [];
        const seenIds = new Set();
        
        for (const product of allProducts) {
            if (!seenIds.has(product._id.toString())) {
                uniqueProducts.push(product);
                seenIds.add(product._id.toString());
            }
        }
        
        // Trier par pertinence
        uniqueProducts.sort((a, b) => {
            if (a.featured && !b.featured) return -1;
            if (!a.featured && b.featured) return 1;
            if (a.rating !== b.rating) return b.rating - a.rating;
            return b.reviewCount - a.reviewCount;
        });
        
        return uniqueProducts.slice(0, 12);
        
    } catch (error) {
        console.error('Erreur recherche produits:', error);
        return [];
    }
}

module.exports = router;
