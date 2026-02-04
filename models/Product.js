const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    category: {
        type: String,
        required: true
    },
    brand: {
        type: String,
        required: true
    },
    price: {
        type: Number,
        required: true
    },
    originalPrice: {
        type: Number
    },
    discountPercentage: {
        type: Number,
        default: 0
    },
    rating: {
        type: Number,
        default: 0
    },
    reviewCount: {
        type: Number,
        default: 0
    },
    qualityScore: {
        type: Number,
        default: 0
    },
    description: {
        type: String
    },
    imageUrl: {
        type: String
    },
    amazonUrl: {
        type: String
    },
    fnacUrl: {
        type: String
    },
    dartyUrl: {
        type: String
    },
    boulangerUrl: {
        type: String
    },
    ldlcUrl: {
        type: String
    },
    cdiscountUrl: {
        type: String
    },
    inStock: {
        type: Boolean,
        default: true
    },
    featured: {
        type: Boolean,
        default: false
    }
}, {
    timestamps: true
});

module.exports = mongoose.model('Product', productSchema);
