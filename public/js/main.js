// Main JavaScript file for SmartChoice

class SmartChoice {
    constructor() {
        this.init();
    }

    init() {
        this.loadFeaturedProducts();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Vision modal
        const visionBtn = document.getElementById('visionBtn');
        const startVision = document.getElementById('startVision');
        const modal = document.getElementById('visionModal');
        const closeBtn = document.querySelector('.close');
        const uploadArea = document.getElementById('uploadArea');
        const imageInput = document.getElementById('imageInput');

        if (visionBtn) {
            visionBtn.addEventListener('click', () => this.openVisionModal());
        }

        if (startVision) {
            startVision.addEventListener('click', () => this.openVisionModal());
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeVisionModal());
        }

        if (uploadArea) {
            uploadArea.addEventListener('click', () => imageInput.click());
        }

        if (imageInput) {
            imageInput.addEventListener('change', (e) => this.handleImageUpload(e));
        }

        // Drag and drop
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#0056b3';
                uploadArea.style.background = 'rgba(0,123,255,0.1)';
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#007bff';
                uploadArea.style.background = 'transparent';
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#007bff';
                uploadArea.style.background = 'transparent';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleImageFile(files[0]);
                }
            });
        }

        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeVisionModal();
            }
        });
    }

    openVisionModal() {
        const modal = document.getElementById('visionModal');
        modal.style.display = 'block';
    }

    closeVisionModal() {
        const modal = document.getElementById('visionModal');
        modal.style.display = 'none';
        
        // Reset results
        document.getElementById('visionResults').style.display = 'none';
        document.getElementById('imageInput').value = '';
    }

    async handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
            await this.handleImageFile(file);
        }
    }

    async handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Veuillez sélectionner une image valide');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        try {
            // Show loading
            const uploadArea = document.getElementById('uploadArea');
            uploadArea.innerHTML = '<i class="fas fa-spinner fa-spin"></i><p>Analyse en cours...</p>';

            const response = await fetch('/api/vision/identify', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showVisionResults(result);
            } else {
                throw new Error(result.error || 'Erreur lors de l\'analyse');
            }
        } catch (error) {
            console.error('Erreur:', error);
            const uploadArea = document.getElementById('uploadArea');
            uploadArea.innerHTML = '<i class="fas fa-exclamation-triangle"></i><p>Erreur lors de l\'analyse</p>';
        }
    }

    showVisionResults(result) {
        const resultsDiv = document.getElementById('visionResults');
        const detectedObjectDiv = document.getElementById('detectedObject');
        const similarProductsDiv = document.getElementById('similarProducts');

        // Show detected object
        detectedObjectDiv.innerHTML = `
            <h5>Objet détecté: ${result.detection.object}</h5>
            <p>Mots-clés: ${result.detection.keywords.join(', ')}</p>
            <p>Confiance: ${(result.detection.confidence * 100).toFixed(0)}%</p>
        `;

        // Show similar products
        if (result.similarProducts && result.similarProducts.length > 0) {
            similarProductsDiv.innerHTML = '<h5>Produits similaires:</h5>';
            const productsGrid = document.createElement('div');
            productsGrid.className = 'products-grid';
            
            result.similarProducts.slice(0, 6).forEach(product => {
                productsGrid.appendChild(this.createProductCard(product));
            });
            
            similarProductsDiv.appendChild(productsGrid);
        } else {
            similarProductsDiv.innerHTML = '<p>Aucun produit similaire trouvé</p>';
        }

        // Show results
        resultsDiv.style.display = 'block';
        
        // Reset upload area
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.innerHTML = '<i class="fas fa-check"></i><p>Analyse terminée!</p>';
    }

    async loadFeaturedProducts() {
        try {
            const response = await fetch('/api/products/featured');
            const data = await response.json();
            
            const container = document.getElementById('featuredProducts');
            if (container) {
                container.innerHTML = '';
                data.products.forEach(product => {
                    container.appendChild(this.createProductCard(product));
                });
            }
        } catch (error) {
            console.error('Erreur lors du chargement des produits:', error);
        }
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        const discountBadge = product.discountPercentage > 0 
            ? `<span class="discount">-${product.discountPercentage}%</span>` 
            : '';
        
        const originalPrice = product.originalPrice && product.originalPrice > product.price
            ? `<span class="original-price">${product.originalPrice.toFixed(2)}€</span>`
            : '';

        card.innerHTML = `
            <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <h4 class="product-name">${product.name}</h4>
                <p class="product-brand">Marque: ${product.brand}</p>
                <div class="product-price">
                    <span class="current-price">${product.price.toFixed(2)}€</span>
                    ${originalPrice}
                    ${discountBadge}
                </div>
                <div class="product-rating">
                    <span class="stars">${this.getStars(product.rating)}</span>
                    <span class="reviews">(${product.reviewCount} avis)</span>
                </div>
                <div class="product-actions">
                    <a href="${product.amazonUrl}" target="_blank" class="btn btn-primary btn-small">
                        <i class="fab fa-amazon"></i> Amazon
                    </a>
                    <a href="${product.fnacUrl}" target="_blank" class="btn btn-outline btn-small">
                        <i class="fas fa-shopping-cart"></i> Fnac
                    </a>
                </div>
            </div>
        `;
        
        return card;
    }

    getStars(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;
        
        let stars = '';
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }
        if (halfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star"></i>';
        }
        
        return stars;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SmartChoice();
});
