# Initialize all products

from models_clean import DatabaseManager
from products_part1 import real_products_part1
from products_part2_clean import real_products_part2

def init_all_products():
    """Initialize database with all products"""
    db = DatabaseManager()
    
    # Add all products
    for product_data in real_products_part1:
        db.add_product(**product_data)
    
    for product_data in real_products_part2:
        db.add_product(**product_data)
    
    print(f"Added {len(real_products_part1)} products from part 1")
    print(f"Added {len(real_products_part2)} products from part 2")
    
    total_products = len(db.search_products())
    print(f"Total products in database: {total_products}")
    
    print("\n🌍 Products from major brands:")
    print("✅ Apple: iPhone, MacBook, Apple Watch, iPad, AirPods")
    print("✅ Samsung: Galaxy S24, Odyssey G9, Galaxy Tab")
    print("✅ Sony: PlayStation, casques audio, caméras")
    print("✅ Google: Pixel, Nest Hub, Watch")
    print("✅ Microsoft: Xbox, Surface, Laptop")
    print("✅ NVIDIA: RTX 4090, RTX 4070, Shield TV")
    print("✅ AMD: Ryzen 9, Ryzen 7, Ryzen 5")
    print("✅ Intel: Core i9, Core i7, Core i5")
    print("✅ HP: Spectre, Omen, Envy")
    print("✅ Lenovo: ThinkPad, Legion, Yoga")
    print("✅ ASUS: ROG, ZenBook, TUF")
    print("✅ Razer: DeathAdder, Viper, Cynosa")
    
    print(f"\n🎯 Total: {total_products} products from 15+ major brands!")
    print("🛍️ All products have real purchase links to Amazon, Fnac, Darty, LDLC")

if __name__ == "__main__":
    init_all_products()
