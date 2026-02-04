// Script pour initialiser la base de données avec les produits

const mongoose = require('mongoose');
const { initializeProducts } = require('./data/products');

require('dotenv').config();

async function seedDatabase() {
    try {
        // Connexion à MongoDB
        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/smartchoice', {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        
        console.log('🔗 Connecté à MongoDB');
        
        // Initialiser les produits
        await initializeProducts();
        
        console.log('✅ Base de données initialisée avec succès!');
        
    } catch (error) {
        console.error('❌ Erreur lors de l\'initialisation:', error);
    } finally {
        await mongoose.disconnect();
        console.log('🔌 Déconnecté de MongoDB');
    }
}

// Exécuter le script
seedDatabase();
