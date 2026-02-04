// Products page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize page
    initializePage();
    
    // Load initial data
    loadFeaturedProducts();
    loadCategories();
    loadBrands();
    
    // Event listeners
    setupEventListeners();
});

// Initialize page
function initializePage() {
    // Check authentication status
    checkAuthStatus();
    
    // Setup search functionality
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    if (searchInput && searchBtn) {
        // Search on button click
        searchBtn.addEventListener('click', performSearch);
        
        // Search on Enter key
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
        
        // Auto-search on input (with debounce)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2) {
                    performSearch();
                } else if (this.value.length === 0) {
                    showFeaturedProducts();
                }
            }, 500);
        });
    }
    
    // Setup filters
    setupFilters();
    
    // Setup modal
    setupModal();
}

// Setup event listeners
function setupEventListeners() {
    // Logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
}

// Setup filters
function setupFilters() {
    const categoryFilter = document.getElementById('category-filter');
    const brandFilter = document.getElementById('brand-filter');
    const minPriceFilter = document.getElementById('min-price');
    const maxPriceFilter = document.getElementById('max-price');
    const sortFilter = document.getElementById('sort-filter');
    
    // Add change event listeners to all filters
    [categoryFilter, brandFilter, minPriceFilter, maxPriceFilter, sortFilter].forEach(filter => {
        if (filter) {
            filter.addEventListener('change', performSearch);
        }
    });
}

// Load featured products
async function loadFeaturedProducts() {
    try {
        showLoading();
        
        const response = await fetch('/api/products/featured?limit=8');
        const result = await response.json();
        
        if (response.ok) {
            displayProducts(result.products, 'featured-products');
        } else {
            console.error('Failed to load featured products');
        }
    } catch (error) {
        console.error('Error loading featured products:', error);
    } finally {
        hideLoading();
    }
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const result = await response.json();
        
        if (response.ok) {
            const categoryFilter = document.getElementById('category-filter');
            const categoriesGrid = document.getElementById('categories-grid');
            
            if (categoryFilter) {
                // Add "All categories" option
                categoryFilter.innerHTML = '<option value="">Toutes les catégories</option>';
                
                // Add categories
                result.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    categoryFilter.appendChild(option);
                });
            }
            
            if (categoriesGrid) {
                // Display categories grid
                categoriesGrid.innerHTML = '';
                result.categories.forEach(category => {
                    const categoryCard = createCategoryCard(category);
                    categoriesGrid.appendChild(categoryCard);
                });
            }
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load brands
async function loadBrands() {
    try {
        const response = await fetch('/api/brands');
        const result = await response.json();
        
        if (response.ok) {
            const brandFilter = document.getElementById('brand-filter');
            
            if (brandFilter) {
                // Add "All brands" option
                brandFilter.innerHTML = '<option value="">Toutes les marques</option>';
                
                // Add brands
                result.brands.forEach(brand => {
                    const option = document.createElement('option');
                    option.value = brand;
                    option.textContent = brand;
                    brandFilter.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading brands:', error);
    }
}

// Perform search
async function performSearch() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const brandFilter = document.getElementById('brand-filter');
    const minPriceFilter = document.getElementById('min-price');
    const maxPriceFilter = document.getElementById('max-price');
    const sortFilter = document.getElementById('sort-filter');
    
    const searchParams = {
        query: searchInput ? searchInput.value : '',
        category: categoryFilter ? categoryFilter.value : '',
        brand: brandFilter ? brandFilter.value : '',
        min_price: minPriceFilter ? parseFloat(minPriceFilter.value) : null,
        max_price: maxPriceFilter ? parseFloat(maxPriceFilter.value) : null,
        sort_by: sortFilter ? sortFilter.value : 'relevance'
    };
    
    try {
        showLoading();
        
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displaySearchResults(result.products, result.total, result.query);
        } else {
            showError('La recherche a échoué');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Une erreur est survenue lors de la recherche');
    } finally {
        hideLoading();
    }
}

// Display products
function displayProducts(products, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

// Display search results
function displaySearchResults(products, total, query) {
    const featuredSection = document.querySelector('.featured-section');
    const resultsSection = document.getElementById('results-section');
    const resultsCount = document.getElementById('results-count');
    const searchResults = document.getElementById('search-results');
    
    // Hide featured section, show results section
    if (featuredSection) featuredSection.style.display = 'none';
    if (resultsSection) resultsSection.style.display = 'block';
    
    // Update results count
    if (resultsCount) {
        if (query) {
            resultsCount.textContent = `${total} résultat(s) pour "${query}"`;
        } else {
            resultsCount.textContent = `${total} produit(s) trouvé(s)`;
        }
    }
    
    // Display products
    if (searchResults) {
        searchResults.innerHTML = '';
        
        if (products.length === 0) {
            searchResults.innerHTML = '<p class="no-results">Aucun produit trouvé</p>';
        } else {
            products.forEach(product => {
                const productCard = createProductCard(product);
                searchResults.appendChild(productCard);
            });
        }
    }
}

// Show featured products
function showFeaturedProducts() {
    const featuredSection = document.querySelector('.featured-section');
    const resultsSection = document.getElementById('results-section');
    
    if (featuredSection) featuredSection.style.display = 'block';
    if (resultsSection) resultsSection.style.display = 'none';
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.onclick = () => showProductModal(product);
    
    const discountBadge = product.discount_percentage > 0 ? 
        `<span class="discount-badge">-${product.discount_percentage}%</span>` : '';
    
    const originalPrice = product.original_price && product.original_price > product.price ?
        `<span class="original-price">${product.original_price}€</span>` : '';
    
    card.innerHTML = `
        <div class="product-image">
            <img src="${product.image_url || '/static/images/placeholder.jpg'}" alt="${product.name}">
            ${discountBadge}
        </div>
        <div class="product-info">
            <h3 class="product-name">${product.name}</h3>
            <p class="product-brand">${product.brand}</p>
            <div class="product-rating">
                ${createStars(product.rating)}
                <span class="review-count">(${product.review_count})</span>
            </div>
            <div class="product-price">
                <span class="current-price">${product.price}€</span>
                ${originalPrice}
            </div>
            <div class="product-retailers">
                ${getAvailableRetailers(product)}
            </div>
        </div>
    `;
    
    return card;
}

// Create category card
function createCategoryCard(category) {
    const card = document.createElement('div');
    card.className = 'category-card';
    card.onclick = () => filterByCategory(category);
    
    const categoryIcons = {
        'electronics': '💻',
        'smartphones': '📱',
        'laptops': '💻',
        'graphics_cards': '🎮',
        'processors': '⚡',
        'monitors': '🖥️',
        'gaming_consoles': '🎮',
        'smartwatches': '⌚'
    };
    
    card.innerHTML = `
        <div class="category-icon">${categoryIcons[category] || '📦'}</div>
        <h3>${category}</h3>
    `;
    
    return card;
}

// Create star rating
function createStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '⭐';
    }
    
    if (hasHalfStar) {
        stars += '⭐';
    }
    
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
        stars += '☆';
    }
    
    return stars;
}

// Get available retailers
function getAvailableRetailers(product) {
    const retailers = [];
    
    if (product.amazon_url) retailers.push('Amazon');
    if (product.fnac_url) retailers.push('Fnac');
    if (product.darty_url) retailers.push('Darty');
    if (product.boulanger_url) retailers.push('Boulanger');
    if (product.ldlc_url) retailers.push('LDLC');
    if (product.cdiscount_url) retailers.push('Cdiscount');
    
    return `<div class="available-retailers">Disponible chez: ${retailers.join(', ')}</div>`;
}

// Filter by category
function filterByCategory(category) {
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.value = category;
        performSearch();
    }
}

// Setup modal
function setupModal() {
    const modal = document.getElementById('product-modal');
    const closeBtn = modal ? modal.querySelector('.close') : null;
    
    if (closeBtn) {
        closeBtn.onclick = () => {
            modal.style.display = 'none';
        };
    }
    
    // Close modal when clicking outside
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}

// Show product modal
function showProductModal(product) {
    const modal = document.getElementById('product-modal');
    if (!modal) return;
    
    // Update modal content
    const modalImage = document.getElementById('modal-product-image');
    const modalName = document.getElementById('modal-product-name');
    const modalBrand = document.getElementById('modal-product-brand');
    const modalPrice = document.getElementById('modal-product-price');
    const modalOriginalPrice = document.getElementById('modal-product-original-price');
    const modalDiscount = document.getElementById('modal-product-discount');
    const modalRating = document.getElementById('modal-product-rating');
    const modalReviewCount = document.getElementById('modal-product-review-count');
    const modalDescription = document.getElementById('modal-product-description');
    const retailerButtons = document.getElementById('retailer-buttons');
    
    if (modalImage) modalImage.src = product.image_url || '/static/images/placeholder.jpg';
    if (modalName) modalName.textContent = product.name;
    if (modalBrand) modalBrand.textContent = product.brand;
    if (modalPrice) modalPrice.textContent = `${product.price}€`;
    if (modalOriginalPrice) {
        modalOriginalPrice.textContent = product.original_price ? `${product.original_price}€` : '';
        modalOriginalPrice.style.display = product.original_price ? 'block' : 'none';
    }
    if (modalDiscount) {
        modalDiscount.textContent = product.discount_percentage > 0 ? `-${product.discount_percentage}%` : '';
        modalDiscount.style.display = product.discount_percentage > 0 ? 'block' : 'none';
    }
    if (modalRating) modalRating.innerHTML = createStars(product.rating);
    if (modalReviewCount) modalReviewCount.textContent = `(${product.review_count} avis)`;
    if (modalDescription) modalDescription.textContent = product.description;
    
    // Add retailer buttons
    if (retailerButtons) {
        retailerButtons.innerHTML = '';
        
        if (product.amazon_url) {
            const btn = createRetailerButton('Amazon', product.amazon_url, '#ff9900');
            retailerButtons.appendChild(btn);
        }
        if (product.fnac_url) {
            const btn = createRetailerButton('Fnac', product.fnac_url, '#e31e24');
            retailerButtons.appendChild(btn);
        }
        if (product.darty_url) {
            const btn = createRetailerButton('Darty', product.darty_url, '#0066cc');
            retailerButtons.appendChild(btn);
        }
        if (product.boulanger_url) {
            const btn = createRetailerButton('Boulanger', product.boulanger_url, '#ff6600');
            retailerButtons.appendChild(btn);
        }
        if (product.ldlc_url) {
            const btn = createRetailerButton('LDLC', product.ldlc_url, '#0099ff');
            retailerButtons.appendChild(btn);
        }
        if (product.cdiscount_url) {
            const btn = createRetailerButton('Cdiscount', product.cdiscount_url, '#ff6600');
            retailerButtons.appendChild(btn);
        }
    }
    
    // Show modal
    modal.style.display = 'block';
}

// Create retailer button
function createRetailerButton(name, url, color) {
    const button = document.createElement('button');
    button.className = 'retailer-button';
    button.textContent = `Acheter sur ${name}`;
    button.style.backgroundColor = color;
    button.onclick = () => window.open(url, '_blank');
    return button;
}

// Show loading
function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'flex';
    }
}

// Hide loading
function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }
}

// Show error
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
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 300px;
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Check auth status
function checkAuthStatus() {
    const token = localStorage.getItem('smartchoice_token');
    const user = localStorage.getItem('smartchoice_user');
    
    if (token && user) {
        updateUIForLoggedInUser(JSON.parse(user));
    }
}

// Update UI for logged in user
function updateUIForLoggedInUser(user) {
    const loginLink = document.getElementById('login-link');
    const userDropdown = document.getElementById('user-dropdown');
    const userName = document.getElementById('user-name');
    
    if (loginLink && userDropdown) {
        loginLink.style.display = 'none';
        userDropdown.style.display = 'block';
        
        if (userName) {
            userName.textContent = `${user.first_name} ${user.last_name}`;
        }
    }
}

// Logout
function logout() {
    localStorage.removeItem('smartchoice_token');
    localStorage.removeItem('smartchoice_user');
    window.location.href = '/';
}
