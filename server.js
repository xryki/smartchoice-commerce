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

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Routes API
app.use('/api/products', productRoutes);
app.use('/api/vision', visionRoutes);

// Routes Frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/products', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route de test
app.get('/test', (req, res) => {
    res.json({ message: 'SmartChoice API fonctionne!', timestamp: new Date() });
});

// Start Server
app.listen(PORT, () => {
    console.log(`Serveur SmartChoice lancé sur le port ${PORT}`);
    console.log(`URL locale: http://localhost:${PORT}`);
    console.log(`URL publique: ${process.env.RAILWAY_PUBLIC_DOMAIN ? `https://${process.env.RAILWAY_PUBLIC_DOMAIN}` : process.env.PUBLIC_URL ? process.env.PUBLIC_URL : 'https://smartchoice-commerce.up.railway.app'}`);
    console.log(`Toutes les variables: PORT=${process.env.PORT}, RAILWAY_PUBLIC_DOMAIN=${process.env.RAILWAY_PUBLIC_DOMAIN}, PUBLIC_URL=${process.env.PUBLIC_URL}`);
    console.log('🚀 Site e-commerce SmartChoice en ligne !');
});
