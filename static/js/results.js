// Results page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const searchForm = document.getElementById('search-form');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const searchQuery = document.getElementById('search-query');
    const sortFilter = document.getElementById('sort-filter');
    const brandFilter = document.getElementById('brand-filter');
    
    // Recommendation cards
    const cheapestCard = document.getElementById('cheapest-card');
    const reliableCard = document.getElementById('reliable-card');
    const qualityCard = document.getElementById('quality-card');
    const personalizedCard = document.getElementById('personalized-card');
    
    // Products grid
    const productsGrid = document.getElementById('products-grid');
    
    let currentProducts = [];
    let currentRecommendations = {};
    
    // Handle form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(searchForm);
            const searchParams = {
                budget: formData.get('budget'),
                social_class: formData.get('social_class'),
                product: formData.get('product'),
                category: formData.get('category')
            };
            
            performSearch(searchParams);
        });
    }
    
    // Handle filter changes
    if (sortFilter) {
        sortFilter.addEventListener('change', function() {
            filterAndSortProducts();
        });
    }
    
    if (brandFilter) {
        brandFilter.addEventListener('change', function() {
            filterAndSortProducts();
        });
    }
    
    // Perform search
    async function performSearch(searchParams) {
        showLoading();
        console.log('Searching with params:', searchParams);
        
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchParams)
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error('Search failed');
            }
            
            const data = await response.json();
            console.log('API Response:', data);
            
            currentProducts = data.products || [];
            currentRecommendations = data.recommendations || {};
            
            console.log('Products found:', currentProducts.length);
            console.log('Recommendations:', currentRecommendations);
            
            displayResults(searchParams, data);
            
        } catch (error) {
            console.error('Search error:', error);
            showError('Une erreur est survenue lors de la recherche');
        } finally {
            hideLoading();
        }
    }
    
    // Display results
    function displayResults(searchParams, data) {
        // Update search query display
        if (searchQuery) {
            searchQuery.textContent = searchParams.product;
        }
        
        // Update brand filter
        updateBrandFilter();
        
        // Display recommendations
        displayRecommendations();
        
        // Display all products
        displayAllProducts();
        
        // Show results section
        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    // Display recommendation cards
    function displayRecommendations() {
        // Cheapest product
        if (currentRecommendations.cheapest && cheapestCard) {
            populateRecommendationCard(cheapestCard, currentRecommendations.cheapest);
        }
        
        // Most reliable product
        if (currentRecommendations.most_reliable && reliableCard) {
            populateRecommendationCard(reliableCard, currentRecommendations.most_reliable);
        }
        
        // Best quality product
        if (currentRecommendations.best_quality && qualityCard) {
            populateRecommendationCard(qualityCard, currentRecommendations.best_quality);
        }
        
        // Personalized recommendation
        if (currentRecommendations.personalized && personalizedCard) {
            populateRecommendationCard(personalizedCard, currentRecommendations.personalized);
            
            // Add recommendation reason
            const reasonText = personalizedCard.querySelector('.reason-text');
            if (reasonText && currentRecommendations.personalized.reason) {
                reasonText.textContent = currentRecommendations.personalized.reason;
            }
        }
    }
    
    // Populate a recommendation card
    function populateRecommendationCard(card, product) {
        const nameEl = card.querySelector('.product-name');
        const brandEl = card.querySelector('.product-brand');
        const priceEl = card.querySelector('.product-price');
        const siteEl = card.querySelector('.product-site');
        
        if (nameEl) nameEl.textContent = product.name;
        if (brandEl) brandEl.textContent = product.brand;
        if (priceEl) priceEl.textContent = `${product.price}€`;
        if (siteEl) siteEl.textContent = product.site;
        
        // Add purchase link if available
        if (product.purchase_url) {
            const cardContent = card.querySelector('.card-content');
            const linkButton = document.createElement('button');
            linkButton.className = 'purchase-button';
            linkButton.textContent = 'Acheter maintenant';
            linkButton.onclick = function() {
                window.open(product.purchase_url, '_blank');
            };
            cardContent.appendChild(linkButton);
        }
        
        // Update metrics
        updateMetrics(card, product);
    }
    
    // Update product metrics
    function updateMetrics(card, product) {
        const qualityFill = card.querySelector('.quality-fill');
        const qualityValue = card.querySelector('.metric-value');
        const reliabilityFill = card.querySelector('.reliability-fill');
        const reliabilityValue = card.querySelectorAll('.metric-value')[1];
        
        if (qualityFill && product.quality_score) {
            qualityFill.style.width = `${product.quality_score}%`;
            if (qualityValue) qualityValue.textContent = `${product.quality_score}/100`;
        }
        
        if (reliabilityFill && product.site_reliability) {
            reliabilityFill.style.width = `${product.site_reliability}%`;
            if (reliabilityValue) reliabilityValue.textContent = `${product.site_reliability}/100`;
        }
    }
    
    // Display all products
    function displayAllProducts() {
        if (!productsGrid) return;
        
        productsGrid.innerHTML = '';
        
        currentProducts.forEach(product => {
            const productCard = createProductCard(product);
            productsGrid.appendChild(productCard);
        });
    }
    
    // Create product card
    function createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        // Add click handler to open purchase link
        if (product.purchase_url) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', function() {
                window.open(product.purchase_url, '_blank');
            });
        }
        
        card.innerHTML = `
            <h4>${product.name}</h4>
            <p class="brand">${product.brand}</p>
            <p class="price">${product.price}€</p>
            <p class="site">${product.site}</p>
            ${product.purchase_url ? `<p class="link">Lien d'achat disponible</p>` : ''}
        `;
        
        return card;
    }
    
    // Update brand filter
    function updateBrandFilter() {
        if (!brandFilter) return;
        
        const brands = [...new Set(currentProducts.map(p => p.brand))].sort();
        
        brandFilter.innerHTML = '<option value="">Toutes les marques</option>';
        brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand;
            option.textContent = brand;
            brandFilter.appendChild(option);
        });
    }
    
    // Filter and sort products
    function filterAndSortProducts() {
        if (!productsGrid) return;
        
        let filteredProducts = [...currentProducts];
        
        // Apply brand filter
        if (brandFilter && brandFilter.value) {
            filteredProducts = filteredProducts.filter(p => p.brand === brandFilter.value);
        }
        
        // Apply sorting
        if (sortFilter) {
            switch (sortFilter.value) {
                case 'price':
                    filteredProducts.sort((a, b) => a.price - b.price);
                    break;
                case 'quality':
                    filteredProducts.sort((a, b) => b.quality_score - a.quality_score);
                    break;
                case 'reliability':
                    filteredProducts.sort((a, b) => b.site_reliability - a.site_reliability);
                    break;
                case 'score':
                    filteredProducts.sort((a, b) => b.global_score - a.global_score);
                    break;
            }
        }
        
        // Update display
        productsGrid.innerHTML = '';
        filteredProducts.forEach(product => {
            const productCard = createProductCard(product);
            productsGrid.appendChild(productCard);
        });
    }
    
    // Loading functions
    function showLoading() {
        if (loading) {
            loading.style.display = 'flex';
        }
    }
    
    function hideLoading() {
        if (loading) {
            loading.style.display = 'none';
        }
    }
    
    // Error handling
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            background: #fee;
            color: #c00;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            text-align: center;
        `;
        
        if (resultsSection) {
            resultsSection.appendChild(errorDiv);
        }
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    // Initialize with API data
    // Remove sample data loading - use real API only
});
