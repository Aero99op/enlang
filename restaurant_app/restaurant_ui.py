# # AURA Fine Dining Restaurant UI Design & Styling Specification (.enlgd)

# # 1. EnLang CSS Styling Blocks (Python-inspired Syntax)

# EnLang CSS Style Block: LuxuryTheme
    # CSS Property -> background-color: #070a12;
    # CSS Property -> accent-primary: #f59e0b;
    # CSS Property -> accent-glow: rgba(245, 158, 11, 0.45);
    # CSS Property -> card-background: rgba(18, 24, 38, 0.85);
    # CSS Property -> font-heading: Playfair Display;
    # CSS Property -> font-body: Outfit;

# EnLang CSS Style Block: HeroCard
    # CSS Property -> background: rgba(245, 158, 11, 0.08);
    # CSS Property -> border: 1px solid rgba(245, 158, 11, 0.45);
    # CSS Property -> border-radius: 24px;
    # CSS Property -> padding: 2.5rem;
    # CSS Property -> margin-bottom: 1.5rem;
    # CSS Property -> backdrop-filter: blur(16px);

# EnLang CSS Style Block: DishCard
    # CSS Property -> background: rgba(18, 24, 38, 0.85);
    # CSS Property -> border: 1px solid rgba(255, 255, 255, 0.08);
    # CSS Property -> border-radius: 20px;
    # CSS Property -> padding: 1.75rem;
    # CSS Property -> backdrop-filter: blur(16px);
    # CSS Property -> box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    # CSS Property -> hover-transform: translateY(-5px);

# EnLang CSS Style Block: GoldButton
    # CSS Property -> background: linear-gradient(135deg, #f59e0b, #d97706);
    # CSS Property -> color: #000000;
    # CSS Property -> font-weight: 700;
    # CSS Property -> border-radius: 25px;
    # CSS Property -> padding: 0.85rem 1.8rem;
    # CSS Property -> box-shadow: 0 4px 15px rgba(245, 158, 11, 0.45);
    # CSS Property -> hover-transform: translateY(-2px);

# # 2. UI Layout Components

main_hero = f"""<div class="hero-enlgd"><h2>{"AURA - Fine Dining Gastronomy"}</h2><p>{"Experience Michelin-Starred Gourmet Culinary Artistry"}</p></div>"""

wagyu_card = f"""<div class="card-enlgd"><div class="card-header"><h2>{"Truffle Wagyu Steak"}</h2><span class="card-price">{"$48.50"}</span></div><p class="card-desc">{"Aged Wagyu ribeye with black truffle butter and rosemary reduction."}</p></div>"""
risotto_card = f"""<div class="card-enlgd"><div class="card-header"><h2>{"Saffron Seafood Risotto"}</h2><span class="card-price">{"$34.00"}</span></div><p class="card-desc">{"Arborio rice in lobster bisque with tiger prawns and saffron sprigs."}</p></div>"""
salad_card = f"""<div class="card-enlgd"><div class="card-header"><h2>{"Burrata & Heirloom Salad"}</h2><span class="card-price">{"$18.50"}</span></div><p class="card-desc">{"Italian burrata, heirloom tomatoes, and aged balsamic glaze."}</p></div>"""
dessert_card = f"""<div class="card-enlgd"><div class="card-header"><h2>{"Gold Leaf Chocolate Sphere"}</h2><span class="card-price">{"$22.00"}</span></div><p class="card-desc">{"Dark Belgian chocolate melted with warm caramel praline."}</p></div>"""

book_btn = f"""<button class="btn-enlgd" onclick="switchTab('reservation')">{"Reserve A Table Now"}</button>"""
order_btn = f"""<button class="btn-enlgd" onclick="switchTab('menu')">{"Explore Gourmet Menu"}</button>"""

print('<div class="layout-enlgd">' + ''.join([main_hero, wagyu_card, risotto_card, salad_card, dessert_card, book_btn, order_btn]) + '</div>')