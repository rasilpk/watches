import os
import shutil
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cr7.settings')
django.setup()

from store.models import Product

def seed():
    src_dir = 'products'
    dest_dir = os.path.join('media', 'products')
    os.makedirs(dest_dir, exist_ok=True)

    products_data = [
        {
            'name': 'Navitimer B01 Chronograph 43',
            'brand': 'Breitling',
            'category': 'Chronograph',
            'price': 9600,
            'description': 'The legendary Breitling Navitimer featuring the iconic circular slide rule bezel, self-winding manufacture Caliber 01, and exhibition sapphire caseback.',
            'image_file': 'breitling-navitimer-ab0138211b1p1-large.jpg'
        },
        {
            'name': 'T-Classic Gentleman Chrono',
            'brand': 'Tissot',
            'category': 'Classic',
            'price': 1250,
            'description': 'Swiss precision elegance with sunray dial, polished steel indices, and durable sapphire crystal suited for any formal occasion.',
            'image_file': 'tissot-t-classic-t150-417-22-031-00-large.jpg'
        },
        {
            'name': 'Santos Chronograph Steel & DLC',
            'brand': 'Cartier',
            'category': 'Luxury',
            'price': 10400,
            'description': 'Iconic square geometric bezel with exposed screws, quick-switch strap mechanism, and high precision automatic movement.',
            'image_file': 'CRWSSA0062_2.webp'
        },
        {
            'name': 'RM 41-01 Automatic Skeleton',
            'brand': 'Richard Mille',
            'category': 'Luxury',
            'price': 185000,
            'description': 'Avant-garde ultra-lightweight grade 5 titanium tonneau case featuring skeletonized movement and variable-geometry rotor.',
            'image_file': 'RM41-01-1.avif'
        },
        {
            'name': 'Submariner Date 41mm',
            'brand': 'Rolex',
            'category': 'Sport',
            'price': 14500,
            'description': 'The benchmark underwater timekeeper with Cerachrom ceramic bezel insert, Oystersteel case, and luminescent Chromalight display.',
            'image_file': '4-s3n4vjwfzcimyvyeizqpl6cv-Main.avif'
        },
        {
            'name': 'Carrera Automatic Chronograph',
            'brand': 'TAG Heuer',
            'category': 'Sport',
            'price': 6800,
            'description': 'Inspired by motor racing heritage, featuring a tachymeter scale, ergonomic pushers, and Calibre HEUER02 automatic movement.',
            'image_file': 'WFRphgC1RZCHGDslA0Se_g.png.transform.vaccard.avif'
        },
        {
            'name': 'Royal Oak Chronograph 41mm',
            'brand': 'Audemars Piguet',
            'category': 'Luxury',
            'price': 45000,
            'description': 'Famous octagonal bezel with hexagon screws, Grande Tapisserie pattern dial, and integrated stainless steel bracelet.',
            'image_file': 'download.jfif'
        },
        {
            'name': 'Speedmaster Professional Moonwatch',
            'brand': 'Omega',
            'category': 'Chronograph',
            'price': 7600,
            'description': 'The world-famous timepiece qualified by NASA for spaceflight, featuring Co-Axial Master Chronometer Calibre 3861.',
            'image_file': 'images.jfif'
        },
        {
            'name': 'Calatrava Pure Gold 39mm',
            'brand': 'Patek Philippe',
            'category': 'Classic',
            'price': 29500,
            'description': 'The supreme expression of round wristwatch design, Clous de Paris guilloche bezel, and ultra-thin manual wound movement.',
            'image_file': 'images_1.jfif'
        },
        {
            'name': 'Overseas Self-Winding Diver',
            'brand': 'Vacheron Constantin',
            'category': 'Luxury',
            'price': 32000,
            'description': 'Maltese cross bezel inspiration, blue lacquer dial, soft-iron casing ring for magnetic protection, and interchangeable bracelet system.',
            'image_file': 'images_2.jfif'
        }
    ]

    print("Copying images to media directory...")
    for item in products_data:
        src_path = os.path.join(src_dir, item['image_file'])
        dest_path = os.path.join(dest_dir, item['image_file'])
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied {item['image_file']}")
        else:
            print(f"Warning: {src_path} not found")

    print("\nSeeding product records into database...")
    for item in products_data:
        prod, created = Product.objects.update_or_create(
            name=item['name'],
            defaults={
                'brand': item['brand'],
                'category': item['category'],
                'price': item['price'],
                'description': item['description'],
                'image': f"products/{item['image_file']}",
                'is_featured': True,
                'in_stock': True,
            }
        )
        status = "Created" if created else "Updated"
        print(f"[{status}] {prod.brand} - {prod.name} (${prod.price})")

    print("\nProduct seeding complete! Total products in database:", Product.objects.count())

if __name__ == '__main__':
    seed()
