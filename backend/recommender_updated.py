class SmartChoiceRecommender:
    """
    SmartChoice Recommendation Algorithm
    Analyzes products based on price, quality, reliability and user profile
    """
    
    def __init__(self):
        # Weight configuration for different social classes
        self.weights = {
            'low': {
                'price': 0.5,      # High importance on price
                'quality': 0.2,    # Lower importance on quality
                'reliability': 0.3 # Medium importance on reliability
            },
            'medium': {
                'price': 0.3,      # Medium importance on price
                'quality': 0.4,    # High importance on quality
                'reliability': 0.3 # Medium importance on reliability
            },
            'high': {
                'price': 0.1,      # Low importance on price
                'quality': 0.5,    # Very high importance on quality
                'reliability': 0.4 # High importance on reliability
            }
        }
        
        # Minimum reliability threshold
        self.min_reliability = 60
    
    def calculate_global_score(self, product, social_class):
        """
        Calculate global score for a product based on user's social class
        """
        weights = self.weights.get(social_class, self.weights['medium'])
        
        # Normalize values (0-100 scale)
        price_score = self._calculate_price_score(product['price'])
        quality_score = product.get('quality_score', 0)
        reliability_score = product.get('site_reliability', 0)
        
        # Calculate weighted score
        global_score = (
            weights['price'] * price_score +
            weights['quality'] * quality_score +
            weights['reliability'] * reliability_score
        )
        
        return round(global_score, 2)
    
    def _calculate_price_score(self, price):
        """
        Calculate price score (lower price = higher score)
        """
        # Inverse relationship: lower price gets higher score
        # Using a logarithmic scale for better distribution
        if price <= 0:
            return 100
        
        # Base score calculation (can be adjusted based on market data)
        max_price = 2000  # Maximum expected price
        score = max(0, 100 * (1 - (price / max_price)))
        
        return round(score, 2)
    
    def get_recommendations(self, products, budget, social_class):
        """
        Get personalized recommendations based on products, budget and social class
        """
        if not products:
            return {}
        
        # Filter out unreliable sites
        reliable_products = [
            p for p in products 
            if p.get('site_reliability', 0) >= self.min_reliability
        ]
        
        if not reliable_products:
            # If no reliable products, use all products but warn
            reliable_products = products
        
        # Calculate global scores for all products
        scored_products = []
        for product in reliable_products:
            product_copy = dict(product)
            product_copy['global_score'] = self.calculate_global_score(
                product_copy, social_class
            )
            scored_products.append(product_copy)
        
        # Sort by global score
        scored_products.sort(key=lambda x: x['global_score'], reverse=True)
        
        # Get specific recommendations
        recommendations = {}
        
        # Cheapest product (within budget)
        affordable_products = [p for p in scored_products if p['price'] <= budget]
        if affordable_products:
            recommendations['cheapest'] = min(affordable_products, key=lambda x: x['price'])
        
        # Most reliable product
        if reliable_products:
            recommendations['most_reliable'] = max(
                reliable_products, 
                key=lambda x: x.get('site_reliability', 0)
            )
        
        # Best quality product
        if reliable_products:
            recommendations['best_quality'] = max(
                reliable_products,
                key=lambda x: x.get('quality_score', 0)
            )
        
        # Personalized recommendation
        if scored_products:
            best_match = scored_products[0]
            
            # Add recommendation reason
            reason = self._generate_recommendation_reason(
                best_match, budget, social_class, scored_products
            )
            best_match['reason'] = reason
            
            recommendations['personalized'] = best_match
        
        return recommendations
    
    def _generate_recommendation_reason(self, product, budget, social_class, all_products):
        """
        Generate a human-readable reason for the recommendation
        """
        reasons = []
        
        # Price-based reasoning
        if product['price'] <= budget * 0.8:
            reasons.append("bien en dessous de votre budget")
        elif product['price'] <= budget:
            reasons.append("respecte votre budget")
        else:
            reasons.append("légèrement au-dessus du budget mais justifié par la qualité")
        
        # Quality-based reasoning
        quality_score = product.get('quality_score', 0)
        if quality_score >= 90:
            reasons.append("qualité exceptionnelle")
        elif quality_score >= 80:
            reasons.append("excellente qualité")
        elif quality_score >= 70:
            reasons.append("bonne qualité")
        
        # Reliability-based reasoning
        reliability = product.get('site_reliability', 0)
        if reliability >= 90:
            reasons.append("vendeur très fiable")
        elif reliability >= 80:
            reasons.append("vendeur fiable")
        
        # Social class specific reasoning
        if social_class == 'low':
            if product['price'] <= budget * 0.7:
                reasons.append("excellent rapport qualité-prix pour votre budget")
        elif social_class == 'medium':
            if quality_score >= 80 and reliability >= 80:
                reasons.append("bon équilibre entre qualité et fiabilité")
        elif social_class == 'high':
            if quality_score >= 90:
                reasons.append("produit premium qui justifie l'investissement")
        
        # Combine reasons
        if len(reasons) == 1:
            return reasons[0].capitalize()
        elif len(reasons) == 2:
            return f"{reasons[0].capitalize()} et {reasons[1]}"
        else:
            return f"{reasons[0].capitalize()}, {reasons[1]} et {reasons[2]}"
    
    def get_alternative_recommendations(self, products, budget, social_class, exclude_ids):
        """
        Get alternative recommendations excluding certain products
        """
        filtered_products = [
            p for p in products 
            if p.get('id') not in exclude_ids
        ]
        
        if not filtered_products:
            return []
        
        # Calculate scores and get top alternatives
        scored_products = []
        for product in filtered_products:
            product_copy = dict(product)
            product_copy['global_score'] = self.calculate_global_score(
                product_copy, social_class
            )
            scored_products.append(product_copy)
        
        scored_products.sort(key=lambda x: x['global_score'], reverse=True)
        
        return scored_products[:3]  # Return top 3 alternatives
    
    def analyze_product_trends(self, products):
        """
        Analyze trends in the product dataset
        """
        if not products:
            return {}
        
        # Calculate statistics
        prices = [p['price'] for p in products]
        qualities = [p.get('quality_score', 0) for p in products]
        reliabilities = [p.get('site_reliability', 0) for p in products]
        
        analysis = {
            'price_range': {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices)
            },
            'quality_distribution': {
                'excellent': len([q for q in qualities if q >= 90]),
                'good': len([q for q in qualities if 70 <= q < 90]),
                'average': len([q for q in qualities if 50 <= q < 70]),
                'poor': len([q for q in qualities if q < 50])
            },
            'reliability_distribution': {
                'very_reliable': len([r for r in reliabilities if r >= 90]),
                'reliable': len([r for r in reliabilities if 70 <= r < 90]),
                'moderate': len([r for r in reliabilities if 50 <= r < 70]),
                'unreliable': len([r for r in reliabilities if r < 50])
            }
        }
        
        return analysis
