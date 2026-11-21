import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Product, CartItem, Order, OrderItem, WishlistItem, Review


def seed_initial_data():
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@store.com', 'admin')
        admin_user.first_name = 'Admin Store Manager'
        admin_user.save()

    if not User.objects.filter(username='aarav').exists():
        u = User.objects.create_user('aarav', 'aarav@example.com', '123')
        u.first_name = 'Aarav Sharma'
        u.save()
    else:
        u = User.objects.get(username='aarav')

    if Product.objects.count() == 0:
        initial_products = [
            Product(
                brand='Samsung',
                name='Samsung Galaxy S25 Ultra',
                price=129999,
                mrp=144999,
                stock_count=18,
                category='Flagship Smartphone',
                image_url='https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=900&q=80',
                description='Engineered with aerospace-grade titanium and Galaxy AI. Capture hyper-detailed 200MP shots day or night.',
                specs='6.9-inch QHD+ Dynamic AMOLED 2X (120Hz) | Snapdragon 8 Elite | 200MP Quad Camera | 5000mAh Battery | Built-in S Pen',
                colors_config='Titanium Silverblue:#7a8fa3,Titanium Black:#242528,Titanium Gray:#8f8e8c,Titanium Whitesilver:#e8eaed',
                storage_config='256GB:0,512GB:12000,1TB:30000',
                ram_config='12GB RAM:0,16GB RAM:10000',
                allow_engraving=True
            ),
            Product(
                brand='Samsung',
                name='Samsung Galaxy Z Fold 6',
                price=164999,
                mrp=179999,
                stock_count=9,
                category='Foldable Smartphone',
                image_url='https://images.unsplash.com/photo-1678911820864-e2c567c655d7?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=900&q=80',
                description='Ultra-thin dual-rail FlexHinge foldable smartphone unfolding into an immersive 7.6-inch Dynamic AMOLED 2X tablet.',
                specs='7.6-inch Main + 6.3-inch Cover Dynamic AMOLED 2X | Snapdragon 8 Gen 3 for Galaxy | 50MP Triple Pro Camera | IP48 Armor Aluminum',
                colors_config='Silver Shadow:#a7acb2,Pink:#e4c4c9,Navy:#23314a,Crafted Black:#1f2022',
                storage_config='256GB:0,512GB:12000,1TB:36000',
                ram_config='12GB LPDDR5X:0,16GB LPDDR5X:14000',
                allow_engraving=True
            ),
            Product(
                brand='Samsung',
                name='Samsung Galaxy Book4 Pro 360',
                price=149990,
                mrp=169990,
                stock_count=12,
                category='2-in-1 AI Laptop',
                image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1531297484001-80022131f5a1?auto=format&fit=crop&w=900&q=80',
                description='Ultra-thin convertible powerhouse with 360-degree hinge and anti-reflective 3K AMOLED brilliance.',
                specs='16-inch 3K AMOLED Touchscreen (120Hz) | Intel Core Ultra 7 | Intel Arc Graphics | S Pen Included | 21-Hr Battery',
                colors_config='Moonstone Gray:#6c7075,Platinum Silver:#d4d7dc',
                storage_config='512GB NVMe SSD:0,1TB NVMe SSD:18000',
                ram_config='16GB LPDDR5X:0,32GB LPDDR5X:22000',
                allow_engraving=True
            ),
            Product(
                brand='Apple',
                name='iPhone 16 Pro Max',
                price=144900,
                mrp=154900,
                stock_count=22,
                category='Pro Smartphone',
                image_url='https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1696446701796-da61225697cc?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1591337676887-a217a6970a8a?auto=format&fit=crop&w=900&q=80',
                description='The ultimate iPhone experience with A18 Pro performance and studio-quality 4K 120fps Dolby Vision camera system.',
                specs='6.9-inch Super Retina XDR ProMotion | A18 Pro 6-Core GPU | 48MP Fusion + 5x Telephoto | Grade 5 Titanium',
                colors_config='Desert Titanium:#c7ab88,Natural Titanium:#96938d,White Titanium:#f3f2ee,Black Titanium:#272729',
                storage_config='256GB:0,512GB:20000,1TB:40000',
                ram_config='8GB Unified:0,12GB Pro Memory:12000',
                allow_engraving=True
            ),
            Product(
                brand='Apple',
                name='MacBook Pro 16 M4 Pro',
                price=249900,
                mrp=269900,
                stock_count=7,
                category='Pro Laptop',
                image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80',
                description='Mind-blowing speed and 24-hour battery endurance in a precision-milled Space Black aluminum enclosure.',
                specs='16.2-inch Liquid Retina XDR | Apple M4 Pro 14-Core CPU | 20-Core GPU | Thunderbolt 5 | 24-Hour Battery',
                colors_config='Space Black:#262729,Silver:#d8dade',
                storage_config='512GB SSD:0,1TB SSD:20000,2TB SSD:60000',
                ram_config='24GB Unified Memory:0,48GB Unified Memory:40000',
                allow_engraving=True
            ),
            Product(
                brand='Apple',
                name='iPad Pro M4 13-inch',
                price=119900,
                mrp=129900,
                stock_count=14,
                category='Pro Tablet',
                image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1561154464-82e9adf32764?auto=format&fit=crop&w=900&q=80',
                description='Impossibly thin 5.1mm design with Tandem OLED Ultra Retina XDR display and Apple M4 neural engine.',
                specs='13-inch Ultra Retina XDR Tandem OLED | Apple M4 Chip | Apple Pencil Pro Support | LiDAR Scanner',
                colors_config='Space Black:#2a2b2d,Silver:#dadce0',
                storage_config='256GB Wi-Fi:0,512GB Wi-Fi:20000,1TB Nano-Texture:60000',
                ram_config='8GB RAM:0,16GB RAM:18000',
                allow_engraving=True
            ),
            Product(
                brand='Sony',
                name='Sony WH-1000XM5 ANC',
                price=29990,
                mrp=34990,
                stock_count=25,
                category='Wireless Audio',
                image_url='https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=900&q=80',
                description='Distraction-free studio sound powered by two processors and eight microphones for crystal clarity.',
                specs='Auto NC Optimizer | 8 Microphones | 30-Hour Battery | LDAC Hi-Res Audio | Multipoint Bluetooth 5.2',
                colors_config='Midnight Blue:#233349,Silver:#dedcd6,Black:#1f1f21',
                storage_config='Standard Edition:0,With Hard Travel Case + DAC Cable:4500',
                ram_config='V1 Integrated Processor:0',
                allow_engraving=True
            ),
            Product(
                brand='Sony',
                name='Sony Alpha 7 IV Mirrorless',
                price=214990,
                mrp=242990,
                stock_count=5,
                category='Full-Frame Camera',
                image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1510127034890-ba27508e9f1c?auto=format&fit=crop&w=900&q=80',
                description='33MP full-frame hybrid camera built for cinema-grade 4K 60p video and crisp low-light stills.',
                specs='33MP Exmor R CMOS Sensor | BIONZ XR Engine | 4K 60p 10-bit 4:2:2 | 759-Point Real-Time Eye AF',
                colors_config='Classic Magnesium Black:#222224',
                storage_config='Body Only:0,With FE 28-70mm Lens Kit:22000',
                ram_config='Dual CFexpress + SDXC:0',
                allow_engraving=False
            ),
            Product(
                brand='Sony',
                name='PlayStation 5 Pro Console',
                price=69990,
                mrp=74990,
                stock_count=11,
                category='Next-Gen Gaming',
                image_url='https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=900&q=80',
                gallery_urls='https://images.unsplash.com/photo-1607853202273-797f1c22a38e?auto=format&fit=crop&w=900&q=80,https://images.unsplash.com/photo-1622297845775-5ff3fef71d13?auto=format&fit=crop&w=900&q=80',
                description='Play at 60fps or up to 120fps with advanced ray tracing and PlayStation Spectral Super Resolution.',
                specs='2TB Ultra-High-Speed SSD | Advanced Ray Tracing | Wi-Fi 7 | DualSense Haptic Controller',
                colors_config='Glacier White:#f5f5f7,Cobalt Blue Edition:#2a52be',
                storage_config='2TB SSD Digital:0,2TB SSD + Disc Drive Bundle:11990',
                ram_config='16GB GDDR6 + 2GB DDR5:0',
                allow_engraving=False
            ),
        ]
        Product.objects.bulk_create(initial_products)

        for prod in Product.objects.all():
            Review.objects.create(
                product=prod,
                user=u,
                rating=5,
                comment=f"Build quality and display on the {prod.name} are phenomenal. Delivery from StudioKart arrived next morning!"
            )


def index(request):
    seed_initial_data()
    query = request.GET.get('q', '').strip()
    products = Product.objects.all().order_by('-created_at')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )

    brands = [
        {
            'name': 'Samsung',
            'tagline': 'Official Brand Store',
            'title': 'Samsung Galaxy',
            'desc': 'Explore Galaxy S25 Ultra, Z Fold 6 Foldable, and Galaxy Book4 Pro 360.',
            'image': 'https://images.unsplash.com/photo-1678911820864-e2c567c655d7?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Apple',
            'tagline': 'Apple Flagship Ecosystem',
            'title': 'Apple Store',
            'desc': 'Discover iPhone 16 Pro Max, MacBook Pro M4, and iPad Pro OLED.',
            'image': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Sony',
            'tagline': 'Audio, Camera & Gaming',
            'title': 'Sony Studio',
            'desc': 'Shop WH-1000XM5 ANC headphones, Alpha 7 IV, and PlayStation 5 Pro.',
            'image': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=900&q=80',
        },
    ]
    existing_names = {b['name'].lower() for b in brands}
    for prod in Product.objects.all():
        if prod.brand.lower() not in existing_names:
            existing_names.add(prod.brand.lower())
            brands.append({
                'name': prod.brand,
                'tagline': 'Featured Brand',
                'title': f"{prod.brand} Collection",
                'desc': f"Explore all {prod.brand} devices available in StudioKart.",
                'image': prod.image_url,
            })

    return render(request, 'store/index.html', {
        'products': products,
        'brands': brands,
        'query': query,
    })


def brand_page(request, brand_name):
    seed_initial_data()
    brand_products = Product.objects.filter(brand__iexact=brand_name).order_by('id')
    brand_meta = {
        'samsung': {
            'eyebrow': 'Samsung Galaxy Ecosystem',
            'headline': 'Galaxy AI is here.',
            'sub': 'Inspect 3D previews, configure RAM & storage, read reviews, or order now.',
        },
        'apple': {
            'eyebrow': 'Apple Pro Lineup',
            'headline': 'Power. Precision. Pro.',
            'sub': 'Configure iPhone, MacBook Pro, and iPad Pro in Apple Studio style.',
        },
        'sony': {
            'eyebrow': 'Sony Entertainment & Imaging',
            'headline': 'Be Moved.',
            'sub': 'Studio-grade audio, full-frame mirrorless cameras, and next-gen gaming.',
        },
    }
    meta = brand_meta.get(brand_name.lower(), {
        'eyebrow': f'{brand_name} Official Collection',
        'headline': f'Explore {brand_name}.',
        'sub': f'Customize and order any {brand_name} product instantly.',
    })
    return render(request, 'store/brand.html', {
        'brand_name': brand_name.capitalize() if brand_name.islower() else brand_name,
        'meta': meta,
        'products': brand_products,
    })


def product_detail(request, pk):
    seed_initial_data()
    product = get_object_or_404(Product, pk=pk)
    colors = product.get_colors_list()
    storages = product.get_storage_list()
    rams = product.get_ram_list()
    gallery = product.get_gallery_list()
    reviews = product.reviews.select_related('user').all()
    similar_products = Product.objects.filter(brand__iexact=product.brand).exclude(pk=product.pk)[:3]
    if similar_products.count() < 3:
        extra = Product.objects.exclude(pk=product.pk).exclude(pk__in=[p.pk for p in similar_products])[:3 - similar_products.count()]
        similar_products = list(similar_products) + list(extra)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'colors': colors,
        'storages': storages,
        'rams': rams,
        'gallery': gallery,
        'reviews': reviews,
        'similar_products': similar_products,
        'in_wishlist': in_wishlist,
    })


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=max(1, min(5, rating)),
                comment=comment
            )
            messages.success(request, "Thank you! Your review has been posted.")
    return redirect('product_detail', pk=pk)


def compare_view(request):
    seed_initial_data()
    all_products = Product.objects.all().order_by('brand', 'name')
    p1_id = request.GET.get('p1')
    p2_id = request.GET.get('p2')
    p1 = Product.objects.filter(pk=p1_id).first() if p1_id else all_products.first()
    p2 = Product.objects.filter(pk=p2_id).first() if p2_id else (all_products[3] if all_products.count() > 3 else all_products.last())
    return render(request, 'store/compare.html', {
        'all_products': all_products,
        'p1': p1,
        'p2': p2,
    })


@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    existing = WishlistItem.objects.filter(user=request.user, product=product).first()
    if existing:
        existing.delete()
        messages.info(request, f"Removed {product.name} from Saved Items.")
    else:
        WishlistItem.objects.create(user=request.user, product=product)
        messages.success(request, f"Saved {product.name} to your Wishlist!")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product').order_by('-added_at')
    return render(request, 'store/wishlist.html', {'items': items})


def auth_view(request):
    seed_initial_data()
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            username_or_email = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                try:
                    u_obj = User.objects.get(email__iexact=username_or_email)
                    user = authenticate(request, username=u_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('admin_panel' if user.is_staff else 'index')
            else:
                messages.error(request, "Invalid credentials. Try admin / admin or aarav / 123.")

        elif action == 'signup':
            full_name = request.POST.get('full_name', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = full_name
                user.save()
                login(request, user)
                messages.success(request, f"Account created! Welcome {full_name}.")
                return redirect('index')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('index')


@login_required
def configure_product_action(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.stock_count <= 0:
        messages.error(request, "Sorry, this item is currently out of stock.")
        return redirect('product_detail', pk=pk)

    colors = product.get_colors_list()
    storages = product.get_storage_list()
    rams = product.get_ram_list()

    if request.method == 'POST':
        action_type = request.POST.get('action_type', 'cart')
        selected_color = request.POST.get('selected_color', colors[0]['name'])
        selected_storage = request.POST.get('selected_storage', storages[0]['label'])
        selected_ram = request.POST.get('selected_ram', rams[0]['label'])
        engraving_text = request.POST.get('engraving_text', '').strip()[:30]
    else:
        action_type = 'cart'
        selected_color = colors[0]['name']
        selected_storage = storages[0]['label']
        selected_ram = rams[0]['label']
        engraving_text = ''

    extra_storage = Decimal('0')
    for s in storages:
        if s['label'] == selected_storage:
            extra_storage = Decimal(str(s['extra']))
            break

    extra_ram = Decimal('0')
    for r in rams:
        if r['label'] == selected_ram:
            extra_ram = Decimal(str(r['extra']))
            break

    final_unit_price = product.price + extra_storage + extra_ram

    if action_type == 'order_now':
        request.session['buy_now_custom'] = {
            'product_id': product.id,
            'color': selected_color,
            'storage': selected_storage,
            'ram': selected_ram,
            'engraving': engraving_text,
            'unit_price': str(final_unit_price),
        }
        return redirect('checkout')

    item = CartItem.objects.filter(
        user=request.user,
        product=product,
        selected_color=selected_color,
        selected_storage=selected_storage,
        selected_ram=selected_ram,
        engraving_text=engraving_text
    ).first()

    if item:
        item.quantity += 1
        item.custom_unit_price = final_unit_price
        item.save()
    else:
        CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            selected_color=selected_color,
            selected_storage=selected_storage,
            selected_ram=selected_ram,
            engraving_text=engraving_text,
            custom_unit_price=final_unit_price
        )
    messages.success(request, f"Added {product.name} ({selected_color}, {selected_ram}, {selected_storage}) to bag.")
    return redirect('cart')


@login_required
def cart_view(request):
    if 'buy_now_custom' in request.session:
        del request.session['buy_now_custom']
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(i.subtotal for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required
def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if action == 'inc':
        item.quantity += 1
        item.save()
    elif action == 'dec':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
    elif action == 'remove':
        item.delete()
    return redirect('cart')


@login_required
def checkout_view(request):
    custom_buy = request.session.get('buy_now_custom')
    buy_now_product = None
    cart_items = []

    if custom_buy:
        buy_now_product = get_object_or_404(Product, pk=custom_buy['product_id'])
        base_total = Decimal(custom_buy['unit_price'])
    else:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            messages.warning(request, "Your shopping bag is empty.")
            return redirect('index')
        base_total = sum(i.subtotal for i in cart_items)

    auto_name = request.user.first_name if request.user.first_name else request.user.username

    # Flipkart-style Bank Card Instant Offers & Monthly EMI Plans
    card_offers = {
        'none': {'label': 'UPI / Cash on Delivery (No Card Offer)', 'discount': Decimal('0')},
        'hdfc': {'label': 'HDFC Bank Credit/Debit Card (10% Instant Off up to ₹5,000)', 'discount': min(Decimal('5000'), (base_total * Decimal('0.10')).quantize(Decimal('1')))},
        'icici': {'label': 'ICICI Bank Credit Card (Flat ₹4,000 Instant Off)', 'discount': min(Decimal('4000'), base_total)},
        'sbi': {'label': 'SBI Credit Card (Flat ₹3,500 Instant Off)', 'discount': min(Decimal('3500'), base_total)},
        'axis': {'label': 'Flipkart Axis Bank Card (5% Unlimited Cashback)', 'discount': (base_total * Decimal('0.05')).quantize(Decimal('1'))},
    }

    if request.method == 'POST':
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()
        payment_mode = request.POST.get('payment_mode', 'full')
        selected_bank = request.POST.get('selected_bank', 'none')
        emi_tenure = int(request.POST.get('emi_tenure', 6))

        offer = card_offers.get(selected_bank, card_offers['none'])
        discount_amt = offer['discount']
        final_payable = max(Decimal('0'), base_total - discount_amt)

        if payment_mode == 'emi':
            # No-Cost EMI for 3 & 6 months; 14% p.a. reducing interest for 9, 12, 24 months
            if emi_tenure in (3, 6):
                monthly_emi = (final_payable / Decimal(emi_tenure)).quantize(Decimal('1'))
                emi_summary = f"{emi_tenure} Months No-Cost EMI @ ₹{monthly_emi:,}/mo"
            else:
                annual_rate = Decimal('0.14')
                r = annual_rate / Decimal('12')
                factor = (1 + r) ** emi_tenure
                monthly_emi = ((final_payable * r * factor) / (factor - 1)).quantize(Decimal('1'))
                emi_summary = f"{emi_tenure} Months Easy EMI @ ₹{monthly_emi:,}/mo (14% p.a.)"
            pay_label = f"Monthly EMI ({offer['label'].split('(')[0].strip()})"
        else:
            emi_summary = ''
            pay_label = offer['label'].split('(')[0].strip()

        order_num = f"ORD-{uuid.uuid4().hex[:6].upper()}"

        order = Order.objects.create(
            order_number=order_num,
            user=request.user,
            customer_name=auto_name,
            mobile=mobile,
            address=address,
            total_amount=final_payable,
            card_discount=discount_amt,
            payment_method=pay_label,
            emi_plan=emi_summary,
            status='Confirmed'
        )

        if custom_buy and buy_now_product:
            config_str = f"{custom_buy['color']} • {custom_buy['ram']} • {custom_buy['storage']}"
            if custom_buy.get('engraving'):
                config_str += f" • Engraved: '{custom_buy['engraving']}'"
            OrderItem.objects.create(
                order=order,
                product_name=buy_now_product.name,
                configuration=config_str,
                price=Decimal(custom_buy['unit_price']),
                quantity=1
            )
            if buy_now_product.stock_count > 0:
                buy_now_product.stock_count -= 1
                buy_now_product.save()
            del request.session['buy_now_custom']
        else:
            for ci in cart_items:
                config_str = f"{ci.selected_color} • {ci.selected_ram} • {ci.selected_storage}"
                if ci.engraving_text:
                    config_str += f" • Engraved: '{ci.engraving_text}'"
                OrderItem.objects.create(
                    order=order,
                    product_name=ci.product.name,
                    configuration=config_str,
                    price=ci.unit_price,
                    quantity=ci.quantity
                )
                if ci.product.stock_count >= ci.quantity:
                    ci.product.stock_count -= ci.quantity
                    ci.product.save()
            cart_items.delete()

        messages.success(request, f"Order {order_num} placed successfully!")
        return redirect('orders')

    return render(request, 'store/checkout.html', {
        'auto_name': auto_name,
        'buy_now_product': buy_now_product,
        'custom_buy': custom_buy,
        'cart_items': cart_items,
        'total': base_total,
    })


@login_required
def orders_view(request):
    if request.user.is_staff:
        orders = Order.objects.all().prefetch_related('items').order_by('-created_at')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.can_cancel:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order {order.order_number} has been cancelled.")
    else:
        messages.error(request, "Cancellation window (24 hours) has expired or order is already cancelled.")
    return redirect('orders')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_panel(request):
    edit_id = request.GET.get('edit')
    edit_product = Product.objects.filter(pk=edit_id).first() if edit_id else None

    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        brand = request.POST.get('brand')
        name = request.POST.get('name')
        price = request.POST.get('price')
        mrp = request.POST.get('mrp') or price
        stock_count = request.POST.get('stock_count') or 10
        category = request.POST.get('category')
        image_url = request.POST.get('image_url')
        gallery_urls = request.POST.get('gallery_urls', '')
        description = request.POST.get('description')
        specs = request.POST.get('specs')
        colors_config = request.POST.get('colors_config') or "Natural Titanium:#8e8d8a,Black Titanium:#2c2c2e"
        storage_config = request.POST.get('storage_config') or "256GB:0,512GB:15000"
        ram_config = request.POST.get('ram_config') or "12GB RAM:0,16GB RAM:10000"
        allow_engraving = request.POST.get('allow_engraving') == 'on'

        if prod_id:
            p = get_object_or_404(Product, pk=prod_id)
            p.brand = brand
            p.name = name
            p.price = price
            p.mrp = mrp
            p.stock_count = stock_count
            p.category = category
            p.image_url = image_url
            p.gallery_urls = gallery_urls
            p.description = description
            p.specs = specs
            p.colors_config = colors_config
            p.storage_config = storage_config
            p.ram_config = ram_config
            p.allow_engraving = allow_engraving
            p.save()
            messages.success(request, f"Updated {p.name}!")
        else:
            Product.objects.create(
                brand=brand,
                name=name,
                price=price,
                mrp=mrp,
                stock_count=stock_count,
                category=category,
                image_url=image_url,
                gallery_urls=gallery_urls,
                description=description,
                specs=specs,
                colors_config=colors_config,
                storage_config=storage_config,
                ram_config=ram_config,
                allow_engraving=allow_engraving
            )
            messages.success(request, f"Added new product: {name}!")
        return redirect('admin_panel')

    products = Product.objects.all().order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'store/admin_panel.html', {
        'products': products,
        'users': users,
        'edit_product': edit_product,
    })


@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f"Deleted {name}.")
    return redirect('admin_panel')
