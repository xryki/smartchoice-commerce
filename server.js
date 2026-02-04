const express = require('express');
const cors = require('cors');
const path = require('path');

// Routes
const productRoutes = require('./routes/products');
const visionRoutes = require('./routes/vision');

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Debug middleware
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Routes API
app.use('/api/products', productRoutes);
app.use('/api/vision', visionRoutes);

// Route de test
app.get('/test', (req, res) => {
    res.json({ message: 'SmartChoice API fonctionne!', timestamp: new Date() });
});

// Route racine
app.get('/', (req, res) => {
    console.log('Servir index.html depuis:', path.join(__dirname, 'public', 'index.html'));
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Toutes les autres routes retournent aussi index.html (SPA)
app.get('*', (req, res) => {
    console.log('Route catch-all:', req.url);
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start Server
app.listen(PORT, () => {
    console.log(`Serveur SmartChoice lancé sur le port ${PORT}`);
    console.log(`URL locale: http://localhost:${PORT}`);
    console.log(`URL publique: ${process.env.RAILWAY_PUBLIC_DOMAIN ? `https://${process.env.RAILWAY_PUBLIC_DOMAIN}` : process.env.PUBLIC_URL ? process.env.PUBLIC_URL : 'https://smartchoice-commerce.up.railway.app'}`);
    console.log(`Toutes les variables: PORT=${process.env.PORT}, RAILWAY_PUBLIC_DOMAIN=${process.env.RAILWAY_PUBLIC_DOMAIN}, PUBLIC_URL=${process.env.PUBLIC_URL}`);
    console.log('🚀 Site e-commerce SmartChoice en ligne !');
});
