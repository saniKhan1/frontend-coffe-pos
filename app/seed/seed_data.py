"""Database seeding with realistic coffee shop data.

Seeds categories, items, addons, customers, discounts, shifts,
expenses, and sample orders to ensure dashboard APIs return meaningful data.
"""

import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.models.addon import Addon
from app.models.category import Category
from app.models.customer import Customer
from app.models.discount import Discount
from app.models.expense import Expense
from app.models.item import Item
from app.models.order import Order, OrderItem, OrderItemAddon
from app.models.shift import Shift
from app.utils.logger import get_logger

logger = get_logger(__name__)


# ─── Seed Data Definitions ────────────────────────────────

CATEGORIES = [
    {"name": "Hot Coffee", "description": "Freshly brewed hot coffee drinks", "display_order": 1},
    {"name": "Cold Coffee", "description": "Refreshing iced and blended coffee drinks", "display_order": 2},
    {"name": "Tea & Non-Coffee", "description": "Teas, hot chocolate, and other non-coffee beverages", "display_order": 3},
    {"name": "Pastries & Bakery", "description": "Fresh pastries, muffins, and baked goods", "display_order": 4},
    {"name": "Snacks & Sandwiches", "description": "Light meals, sandwiches, and savory snacks", "display_order": 5},
    {"name": "Add-on Extras", "description": "Extra shots, syrups, and milk alternatives", "display_order": 6},
]

ITEMS = {
    "Hot Coffee": [
        {"name": "Espresso", "description": "Rich and bold single shot of espresso", "price": 3.25, "stock_qty": -1},
        {"name": "Double Espresso", "description": "Intense double shot of pure espresso", "price": 4.50, "stock_qty": -1},
        {"name": "Americano", "description": "Espresso diluted with hot water for a smooth taste", "price": 4.00, "stock_qty": -1},
        {"name": "Cappuccino", "description": "Equal parts espresso, steamed milk, and foam", "price": 4.75, "stock_qty": -1},
        {"name": "Caramel Latte", "description": "Espresso with steamed milk and rich caramel syrup", "price": 5.50, "stock_qty": -1},
        {"name": "Vanilla Latte", "description": "Smooth espresso with vanilla-infused steamed milk", "price": 5.50, "stock_qty": -1},
        {"name": "Mocha", "description": "Espresso blended with chocolate and steamed milk", "price": 5.75, "stock_qty": -1},
        {"name": "Flat White", "description": "Velvety microfoam over a double ristretto", "price": 4.75, "stock_qty": -1},
        {"name": "Hazelnut Latte", "description": "Espresso with hazelnut syrup and steamed milk", "price": 5.50, "stock_qty": -1},
        {"name": "Macchiato", "description": "Espresso marked with a dollop of foamed milk", "price": 4.25, "stock_qty": -1},
    ],
    "Cold Coffee": [
        {"name": "Iced Americano", "description": "Espresso over ice with cold water", "price": 4.25, "stock_qty": -1},
        {"name": "Iced Latte", "description": "Espresso with cold milk over ice", "price": 5.25, "stock_qty": -1},
        {"name": "Iced Caramel Latte", "description": "Chilled caramel latte over ice", "price": 5.75, "stock_qty": -1},
        {"name": "Iced Mocha", "description": "Chocolate espresso blended with ice and milk", "price": 6.25, "stock_qty": -1},
        {"name": "Cold Brew", "description": "Slow-steeped cold brew coffee, smooth and bold", "price": 4.75, "stock_qty": -1},
        {"name": "Caramel Frappuccino", "description": "Blended ice coffee with caramel and whipped cream", "price": 6.50, "stock_qty": -1},
        {"name": "Mocha Frappuccino", "description": "Blended chocolate coffee with ice and cream", "price": 6.50, "stock_qty": -1},
        {"name": "Vanilla Cold Brew", "description": "Cold brew with vanilla sweet cream", "price": 5.25, "stock_qty": -1},
    ],
    "Tea & Non-Coffee": [
        {"name": "English Breakfast Tea", "description": "Classic black tea, full-bodied and robust", "price": 3.50, "stock_qty": -1},
        {"name": "Green Tea", "description": "Light and refreshing Japanese green tea", "price": 3.50, "stock_qty": -1},
        {"name": "Chai Latte", "description": "Spiced tea with steamed milk", "price": 4.75, "stock_qty": -1},
        {"name": "Matcha Latte", "description": "Premium Japanese matcha with steamed milk", "price": 5.50, "stock_qty": -1},
        {"name": "Hot Chocolate", "description": "Rich chocolate with steamed milk and whipped cream", "price": 4.50, "stock_qty": -1},
        {"name": "Iced Tea", "description": "Refreshing brewed tea served over ice", "price": 3.75, "stock_qty": -1},
    ],
    "Pastries & Bakery": [
        {"name": "Butter Croissant", "description": "Flaky, buttery French croissant", "price": 3.50, "stock_qty": 50},
        {"name": "Chocolate Croissant", "description": "Croissant filled with rich dark chocolate", "price": 4.00, "stock_qty": 40},
        {"name": "Blueberry Muffin", "description": "Moist muffin packed with fresh blueberries", "price": 3.75, "stock_qty": 35},
        {"name": "Banana Nut Muffin", "description": "Banana muffin with crunchy walnuts", "price": 3.75, "stock_qty": 30},
        {"name": "Cinnamon Roll", "description": "Warm cinnamon roll with cream cheese icing", "price": 4.25, "stock_qty": 25},
        {"name": "Scone (Mixed Berry)", "description": "Tender scone with mixed berries and glaze", "price": 3.50, "stock_qty": 30},
        {"name": "Brownie", "description": "Fudgy chocolate brownie", "price": 3.75, "stock_qty": 40},
    ],
    "Snacks & Sandwiches": [
        {"name": "Turkey & Cheese Panini", "description": "Grilled panini with turkey, swiss cheese, and pesto", "price": 7.50, "stock_qty": 20},
        {"name": "Caprese Sandwich", "description": "Fresh mozzarella, tomato, and basil on ciabatta", "price": 7.00, "stock_qty": 15},
        {"name": "Chicken Caesar Wrap", "description": "Grilled chicken with Caesar dressing in a tortilla", "price": 7.25, "stock_qty": 15},
        {"name": "Avocado Toast", "description": "Smashed avocado on sourdough with chili flakes", "price": 6.50, "stock_qty": 20},
        {"name": "Granola Bar", "description": "House-made oat and honey granola bar", "price": 2.50, "stock_qty": 50},
        {"name": "Fruit Cup", "description": "Fresh seasonal mixed fruit cup", "price": 4.50, "stock_qty": 25},
    ],
}

ADDONS = [
    {"name": "Extra Espresso Shot", "price": 0.75},
    {"name": "Vanilla Syrup", "price": 0.50},
    {"name": "Caramel Syrup", "price": 0.50},
    {"name": "Hazelnut Syrup", "price": 0.50},
    {"name": "Oat Milk", "price": 0.60},
    {"name": "Almond Milk", "price": 0.60},
    {"name": "Soy Milk", "price": 0.50},
    {"name": "Coconut Milk", "price": 0.60},
    {"name": "Whipped Cream", "price": 0.50},
    {"name": "Chocolate Drizzle", "price": 0.50},
    {"name": "Cinnamon Sprinkle", "price": 0.25},
    {"name": "Extra Foam", "price": 0.25},
]

CUSTOMERS = [
    {"name": "Alice Johnson", "phone": "+1234567001", "email": "alice@example.com"},
    {"name": "Bob Smith", "phone": "+1234567002", "email": "bob@example.com"},
    {"name": "Carol Williams", "phone": "+1234567003", "email": "carol@example.com"},
    {"name": "David Brown", "phone": "+1234567004", "email": "david@example.com"},
    {"name": "Emma Davis", "phone": "+1234567005", "email": "emma@example.com"},
    {"name": "Frank Miller", "phone": "+1234567006", "email": "frank@example.com"},
    {"name": "Grace Wilson", "phone": "+1234567007", "email": "grace@example.com"},
    {"name": "Henry Moore", "phone": "+1234567008", "email": "henry@example.com"},
]

DISCOUNTS = [
    {"name": "Happy Hour 20%", "type": "percentage", "value": 20.0, "is_active": True},
    {"name": "Student 10% Off", "type": "percentage", "value": 10.0, "is_active": True},
    {"name": "$2 Off Any Order", "type": "flat", "value": 2.0, "is_active": True},
    {"name": "Weekend Special 15%", "type": "percentage", "value": 15.0, "is_active": False},
]

EXPENSE_CATEGORIES = ["supplies", "maintenance", "wages", "utilities", "marketing", "rent", "miscellaneous"]

EXPENSE_DESCRIPTIONS = {
    "supplies": ["Coffee beans restocking", "Milk and cream delivery", "Cups and lids order", "Napkins and straws"],
    "maintenance": ["Espresso machine maintenance", "AC filter replacement", "Plumbing repair"],
    "wages": ["Part-time barista wages", "Weekend staff bonus", "Training session"],
    "utilities": ["Electricity bill", "Water bill", "Internet service"],
    "marketing": ["Social media ad campaign", "Flyer printing", "Local event sponsorship"],
    "rent": ["Monthly rent"],
    "miscellaneous": ["Cleaning supplies", "Office supplies", "Decoration items"],
}


def seed_database(db: Session) -> None:
    """Seed the database with initial data if tables are empty.

    This function is idempotent — it checks if data already exists before seeding.

    Args:
        db: Database session.
    """
    # Check if already seeded
    if db.query(Category).count() > 0:
        logger.info("Database already seeded — skipping")
        return

    logger.info("Seeding database with initial data...")
    random.seed(42)  # Reproducible random data
    now = datetime.now(timezone.utc)

    # ─── Categories ───────────────────────────────
    categories = {}
    for cat_data in CATEGORIES:
        cat = Category(**cat_data)
        db.add(cat)
        db.flush()
        categories[cat.name] = cat
    logger.info(f"Seeded {len(categories)} categories")

    # ─── Items ────────────────────────────────────
    items = []
    for cat_name, item_list in ITEMS.items():
        cat = categories[cat_name]
        for item_data in item_list:
            item = Item(category_id=cat.id, **item_data)
            db.add(item)
            db.flush()
            items.append(item)
    logger.info(f"Seeded {len(items)} items")

    # ─── Addons ───────────────────────────────────
    addons = []
    for addon_data in ADDONS:
        addon = Addon(**addon_data)
        db.add(addon)
        db.flush()
        addons.append(addon)
    logger.info(f"Seeded {len(addons)} addons")

    # ─── Customers ────────────────────────────────
    customers = []
    for cust_data in CUSTOMERS:
        cust = Customer(**cust_data)
        db.add(cust)
        db.flush()
        customers.append(cust)
    logger.info(f"Seeded {len(customers)} customers")

    # ─── Discounts ────────────────────────────────
    discounts = []
    for disc_data in DISCOUNTS:
        disc = Discount(**disc_data)
        db.add(disc)
        db.flush()
        discounts.append(disc)
    logger.info(f"Seeded {len(discounts)} discounts")

    # ─── Shifts ───────────────────────────────────
    shifts = []
    for day_offset in range(30, 0, -1):
        shift_date = now - timedelta(days=day_offset)
        # Morning shift
        morning = Shift(
            opened_at=shift_date.replace(hour=6, minute=0, second=0),
            closed_at=shift_date.replace(hour=14, minute=0, second=0),
            opening_cash=200.0,
            closing_cash=round(200.0 + random.uniform(150, 400), 2),
            status="closed",
            notes=f"Morning shift - Day {day_offset}",
        )
        db.add(morning)
        db.flush()
        shifts.append(morning)

        # Afternoon shift
        afternoon = Shift(
            opened_at=shift_date.replace(hour=14, minute=0, second=0),
            closed_at=shift_date.replace(hour=22, minute=0, second=0),
            opening_cash=200.0,
            closing_cash=round(200.0 + random.uniform(100, 350), 2),
            status="closed",
            notes=f"Afternoon shift - Day {day_offset}",
        )
        db.add(afternoon)
        db.flush()
        shifts.append(afternoon)

    # Add today's open shift
    today_shift = Shift(
        opened_at=now.replace(hour=6, minute=0, second=0),
        opening_cash=200.0,
        status="open",
        notes="Today's shift",
    )
    db.add(today_shift)
    db.flush()
    shifts.append(today_shift)
    logger.info(f"Seeded {len(shifts)} shifts")

    # ─── Expenses ─────────────────────────────────
    expense_count = 0
    for day_offset in range(30, 0, -1):
        exp_date = now - timedelta(days=day_offset)
        # 1-3 expenses per day
        for _ in range(random.randint(1, 3)):
            cat = random.choice(EXPENSE_CATEGORIES)
            desc_options = EXPENSE_DESCRIPTIONS.get(cat, ["General expense"])
            expense = Expense(
                category=cat,
                description=random.choice(desc_options),
                amount=round(random.uniform(15, 250), 2),
                date=exp_date,
                shift_id=random.choice([s.id for s in shifts if s.status == "closed"]),
            )
            db.add(expense)
            expense_count += 1
    db.flush()
    logger.info(f"Seeded {expense_count} expenses")

    # ─── Orders ───────────────────────────────────
    payment_methods = ["cash", "card", "mobile"]
    statuses_completed = ["completed"]  # Most orders should be completed for good dashboard data
    statuses_all = ["completed", "completed", "completed", "completed", "cancelled", "pending", "preparing", "ready"]

    order_count = 0
    order_num = 0
    coffee_items = [i for i in items if i.category_id in [categories["Hot Coffee"].id, categories["Cold Coffee"].id]]
    food_items = [i for i in items if i.category_id in [categories["Pastries & Bakery"].id, categories["Snacks & Sandwiches"].id]]
    drink_addons = addons[:8]  # First 8 addons are drink-related

    for day_offset in range(30, 0, -1):
        order_date = now - timedelta(days=day_offset)
        # 8-20 orders per day for realistic data
        num_orders = random.randint(8, 20)
        day_shifts = [s for s in shifts if s.opened_at.date() == order_date.date() and s.status == "closed"]

        for _ in range(num_orders):
            order_num += 1
            order_hour = random.choices(
                range(6, 22),
                weights=[3, 8, 10, 8, 6, 5, 7, 9, 8, 6, 5, 4, 3, 2, 1, 1],  # Busier mornings
            )[0]
            order_time = order_date.replace(hour=order_hour, minute=random.randint(0, 59), second=random.randint(0, 59))

            # Pick a shift for this order
            shift = None
            if day_shifts:
                for s in day_shifts:
                    if s.opened_at <= order_time <= (s.closed_at or order_time):
                        shift = s
                        break
                if not shift:
                    shift = day_shifts[0]

            # Customer (70% have a customer, 30% walk-in)
            customer = random.choice(customers) if random.random() < 0.7 else None

            # Apply discount (10% of orders)
            discount = None
            discount_amount = 0.0
            if random.random() < 0.1:
                discount = random.choice([d for d in discounts if d.is_active])

            # Status: mostly completed for good dashboard data
            status = random.choice(statuses_all)

            # Build order items (1-4 items)
            order_items = []
            subtotal = 0.0
            num_items = random.randint(1, 4)

            for _ in range(num_items):
                # 70% chance coffee, 30% chance food
                if random.random() < 0.7:
                    item = random.choice(coffee_items)
                else:
                    item = random.choice(food_items)

                qty = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
                addon_total = 0.0
                item_addons = []

                # 40% chance of addons on coffee items
                if item in coffee_items and random.random() < 0.4:
                    num_addons = random.randint(1, 2)
                    selected_addons = random.sample(drink_addons, min(num_addons, len(drink_addons)))
                    for a in selected_addons:
                        item_addons.append(OrderItemAddon(addon_id=a.id, price=a.price))
                        addon_total += a.price

                line_sub = round((item.price + addon_total) * qty, 2)
                oi = OrderItem(
                    item_id=item.id,
                    quantity=qty,
                    unit_price=item.price,
                    subtotal=line_sub,
                )
                oi.addons = item_addons
                order_items.append(oi)
                subtotal += line_sub

            subtotal = round(subtotal, 2)

            # Calculate discount
            if discount:
                if discount.type == "percentage":
                    discount_amount = round(subtotal * (discount.value / 100), 2)
                else:
                    discount_amount = min(discount.value, subtotal)

            tax_amount = round((subtotal - discount_amount) * settings.TAX_RATE, 2)
            total = round(subtotal - discount_amount + tax_amount, 2)

            order_number = f"PHI-{order_date.strftime('%Y%m%d')}-{order_num:04d}"

            order = Order(
                order_number=order_number,
                customer_id=customer.id if customer else None,
                status=status,
                payment_method=random.choice(payment_methods),
                subtotal=subtotal,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                discount_id=discount.id if discount else None,
                total=total,
                shift_id=shift.id if shift else None,
                notes=None,
                created_at=order_time,
                updated_at=order_time,
            )
            order.order_items = order_items
            db.add(order)
            order_count += 1

            # Update customer stats for completed orders
            if customer and status == "completed":
                customer.total_orders += 1
                customer.total_spent = round(customer.total_spent + total, 2)

    db.commit()
    logger.info(f"Seeded {order_count} orders")
    logger.info("Database seeding completed successfully!")
