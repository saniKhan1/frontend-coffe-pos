# ☕ Philo Coffee Shop — Frontend Integration Guide

> **Base URL**: `http://localhost:8000`  
> **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)  
> **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)  
> **📚 Live Documentation**: [https://mrqadeer.github.io/philo-coffee-shop/](https://mrqadeer.github.io/philo-coffee-shop/)

This document explains **every API endpoint**, how they relate to each other, and the **complete flow** of the Philo Coffee Shop POS system. Use this as your single source of truth while building the frontend.

For comprehensive API reference with curl examples and full JSON schemas, see the [Live Documentation](https://mrqadeer.github.io/philo-coffee-shop/).

---

## Table of Contents

- [System Overview](#system-overview)
- [API Flow Diagram](#api-flow-diagram)
- [Authentication](#authentication)
- [Response Conventions](#response-conventions)
- [1. Categories](#1-categories)
- [2. Menu Items](#2-menu-items)
- [3. Add-ons](#3-add-ons)
- [4. Customers](#4-customers)
- [5. Orders (Core Flow)](#5-orders-core-flow)
- [6. Discounts](#6-discounts)
- [7. Shifts](#7-shifts)
- [8. Expenses](#8-expenses)
- [9. Dashboard Analytics](#9-dashboard-analytics)
- [Order Lifecycle Diagram](#order-lifecycle-diagram)
- [Shift Lifecycle Diagram](#shift-lifecycle-diagram)
- [Data Relationship Map](#data-relationship-map)
- [Common Scenarios](#common-scenarios)

---

## System Overview

Philo Coffee Shop POS is a **complete point-of-sale backend** for a coffee shop. The system handles:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHILO COFFEE SHOP POS                        │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│   CATALOG    │  OPERATIONS  │   FINANCE    │    ANALYTICS      │
├──────────────┼──────────────┼──────────────┼───────────────────┤
│ Categories   │ Orders       │ Shifts       │ Dashboard Summary │
│ Items        │ Order Status │ Expenses     │ Revenue Trends    │
│ Addons       │ Customers    │ Discounts    │ Top Items         │
│              │              │              │ Customer Insights │
│              │              │              │ Profit & Loss     │
│              │              │              │ Hourly Heatmap    │
└──────────────┴──────────────┴──────────────┴───────────────────┘
```

---

## API Flow Diagram

This diagram shows how all API resources connect and the typical order of operations:

```
                              ┌──────────────┐
                              │   START DAY  │
                              └──────┬───────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   POST /shifts/open  │
                          │  (Open a new shift)  │
                          └──────────┬──────────┘
                                     │
              ┌──────────────────────┼───────────────────────┐
              │                      │                       │
              ▼                      ▼                       ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐
   │  GET /categories  │  │  GET /customers   │  │   GET /discounts   │
   │  GET /items       │  │  (lookup/create)  │  │   (active ones)    │
   │  GET /addons      │  │                   │  │                    │
   │  (Load menu)      │  │                   │  │                    │
   └────────┬─────────┘  └────────┬──────────┘  └─────────┬──────────┘
            │                      │                       │
            └──────────────────────┼───────────────────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │    POST /orders        │
                       │  (Create new order)    │
                       │  items + addons +      │
                       │  customer + discount   │
                       └───────────┬───────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌──────────┐  ┌──────────────┐  ┌──────────┐
            │ PENDING  │  │  PREPARING   │  │  READY   │
            │          ├─►│              ├─►│          │
            └──┬───────┘  └──────┬───────┘  └──┬───────┘
               │                 │              │
               │    ┌────────────┘              │
               │    │                           │
               ▼    ▼                           ▼
          ┌──────────────┐              ┌──────────────┐
          │  CANCELLED   │              │  COMPLETED   │
          └──────────────┘              └──────────────┘
                                               │
                                   ┌───────────┼───────────┐
                                   │                       │
                                   ▼                       ▼
                          ┌────────────────┐     ┌──────────────────┐
                          │ POST /expenses │     │ GET /dashboard/* │
                          │ (Track costs)  │     │ (View analytics) │
                          └────────────────┘     └──────────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ PATCH /shifts/{id}/close │
                        │    (End of day)          │
                        └─────────────────────────┘
```

---

## Authentication

**There is no authentication.** All endpoints are open. You can call any endpoint directly without tokens or headers.

---

## Response Conventions

### Paginated Lists

All list endpoints (`GET /categories`, `GET /items`, `GET /orders`, etc.) return a paginated envelope:

```json
{
  "items": [ ... ],       // Array of resources
  "total": 42,            // Total matching records
  "page": 1,              // Current page (1-indexed)
  "per_page": 20,         // Items per page
  "total_pages": 3        // Calculated total pages
}
```

**Query params for pagination:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | `1` | Page number (starts at 1) |
| `per_page` | int | `20` | Items per page (max 100) |

### Success Responses

| Action | Status Code | Body |
|--------|-------------|------|
| Create | `201` | Created resource object |
| Read | `200` | Resource object or paginated list |
| Update | `200` | Updated resource object |
| Delete | `200` | `{"message": "... deleted successfully"}` |

### Error Responses

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad request (validation error, invalid transition) |
| `404` | Resource not found |
| `409` | Conflict (e.g. opening shift when one is already open) |
| `422` | Validation error (Pydantic) |

Error body: `{"detail": "Human-readable error message"}`

---

## 1. Categories

> **Purpose**: Group menu items into logical categories displayed in the POS menu.

Categories are the **top-level organizers** for the menu. Each item belongs to exactly one category.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/categories` | List all categories (paginated) |
| `POST` | `/api/v1/categories` | Create a new category |
| `GET` | `/api/v1/categories/{id}` | Get a single category |
| `PATCH` | `/api/v1/categories/{id}` | Update category fields |
| `DELETE` | `/api/v1/categories/{id}` | Delete (fails if items exist) |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `is_active` | bool | Show only active/inactive categories |
| `search` | string | Search in category name |

### Create/Update Body

```json
{
  "name": "Hot Coffee",              // required, unique
  "description": "Freshly brewed",   // optional
  "display_order": 1,                // sort priority (default 0)
  "is_active": true                  // default true
}
```

### Response Shape

```json
{
  "id": 1,
  "name": "Hot Coffee",
  "description": "Freshly brewed hot coffee drinks",
  "display_order": 1,
  "is_active": true,
  "created_at": "2026-03-01T06:00:00",
  "updated_at": "2026-03-01T06:00:00"
}
```

**Pre-seeded categories:** Hot Coffee, Cold Coffee, Tea & Non-Coffee, Pastries & Bakery, Snacks & Sandwiches, Add-on Extras

---

## 2. Menu Items

> **Purpose**: Individual products that can be ordered. Each item belongs to a category and has a price.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/items` | List items (paginated, filterable) |
| `POST` | `/api/v1/items` | Create a new menu item |
| `GET` | `/api/v1/items/{id}` | Get item detail with category |
| `PATCH` | `/api/v1/items/{id}` | Update item fields |
| `DELETE` | `/api/v1/items/{id}` | Delete an item |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `category_id` | int | Filter by category |
| `is_available` | bool | Only available/unavailable items |
| `search` | string | Search in name and description |
| `min_price` | float | Minimum price filter |
| `max_price` | float | Maximum price filter |

### Create/Update Body

```json
{
  "name": "Caramel Latte",
  "description": "Espresso with steamed milk and caramel",
  "price": 5.50,              // required, > 0
  "category_id": 1,           // required
  "stock_qty": -1,            // -1 = unlimited stock
  "is_available": true
}
```

### Response Shape

```json
{
  "id": 5,
  "category_id": 1,
  "category_name": "Hot Coffee",
  "name": "Caramel Latte",
  "description": "Espresso with steamed milk and rich caramel syrup",
  "price": 5.50,
  "image_url": null,
  "is_available": true,
  "stock_qty": -1,
  "created_at": "2026-03-01T06:00:00",
  "updated_at": "2026-03-01T06:00:00"
}
```

### Stock Behavior

| `stock_qty` Value | Meaning |
|-------------------|---------|
| `-1` | Unlimited (drinks, etc.) |
| `0` | Out of stock |
| `> 0` | Tracked stock — decremented on each order |

When an order is placed, items with tracked stock get their `stock_qty` reduced. When an order is **cancelled**, stock is **restored**.

---

## 3. Add-ons

> **Purpose**: Extra toppings, syrups, or milk alternatives that customers add to their drinks.

Add-ons are **attached to individual order line items** (not to the order itself).

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/addons` | List all add-ons |
| `POST` | `/api/v1/addons` | Create a new add-on |
| `GET` | `/api/v1/addons/{id}` | Get add-on detail |
| `PATCH` | `/api/v1/addons/{id}` | Update an add-on |
| `DELETE` | `/api/v1/addons/{id}` | Delete an add-on |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `is_available` | bool | Filter by availability |
| `search` | string | Search in addon name |

### Create/Update Body

```json
{
  "name": "Extra Espresso Shot",
  "price": 0.75,
  "is_available": true
}
```

### Response Shape

```json
{
  "id": 1,
  "name": "Extra Espresso Shot",
  "price": 0.75,
  "is_available": true,
  "created_at": "2026-03-01T06:00:00",
  "updated_at": "2026-03-01T06:00:00"
}
```

**Pre-seeded add-ons:** Extra Espresso Shot, Vanilla Syrup, Caramel Syrup, Hazelnut Syrup, Oat Milk, Almond Milk, Soy Milk, Coconut Milk, Whipped Cream, Chocolate Drizzle, Cinnamon Sprinkle, Extra Foam

---

## 4. Customers

> **Purpose**: Track repeat customers for loyalty, order history, and analytics.

Customers are **optional** on orders — walk-in orders can have `customer_id: null`.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/customers` | List customers (searchable) |
| `POST` | `/api/v1/customers` | Register a new customer |
| `GET` | `/api/v1/customers/{id}` | Get customer profile |
| `GET` | `/api/v1/customers/{id}/orders` | Get all orders for a customer |
| `PATCH` | `/api/v1/customers/{id}` | Update customer info |
| `DELETE` | `/api/v1/customers/{id}` | Delete a customer |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `search` | string | Search by name, phone, or email |

### Create/Update Body

```json
{
  "name": "Alice Johnson",
  "phone": "+1234567001",
  "email": "alice@example.com"
}
```

### Response Shape

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "phone": "+1234567001",
  "email": "alice@example.com",
  "total_orders": 15,
  "total_spent": 127.50,
  "created_at": "2026-03-01T06:00:00",
  "updated_at": "2026-03-01T06:00:00"
}
```

> `total_orders` and `total_spent` are **auto-updated** whenever a customer's order is completed.

---

## 5. Orders (Core Flow)

> **Purpose**: The heart of the POS system. Create orders, track their status through the kitchen, and complete them.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/v1/orders` | Create a new order |
| `GET` | `/api/v1/orders` | List orders (filterable) |
| `GET` | `/api/v1/orders/{id}` | Get full order detail |
| `PATCH` | `/api/v1/orders/{id}/status` | Advance or cancel order |
| `DELETE` | `/api/v1/orders/{id}` | Delete (not completed ones) |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `status` | string | `pending`, `preparing`, `ready`, `completed`, `cancelled` |
| `payment_method` | string | `cash`, `card`, `mobile` |
| `customer_id` | int | Orders by specific customer |
| `shift_id` | int | Orders in a specific shift |
| `start_date` | string | From date (`YYYY-MM-DD`) |
| `end_date` | string | To date (`YYYY-MM-DD`) |

### Creating an Order

This is the **most important API call**. Here's the full create payload:

```json
{
  "customer_id": 1,                    // optional (null = walk-in)
  "payment_method": "card",            // "cash" | "card" | "mobile"
  "discount_id": 1,                    // optional
  "shift_id": 61,                      // optional (link to current shift)
  "notes": "Extra hot, no sugar",      // optional
  "items": [
    {
      "item_id": 5,                    // Caramel Latte
      "quantity": 2,
      "addon_ids": [1, 3]             // Extra Shot + Caramel Syrup
    },
    {
      "item_id": 25,                   // Butter Croissant
      "quantity": 1,
      "addon_ids": []
    }
  ]
}
```

### What happens when you create an order:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORDER CREATION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Validate all item_ids exist and are available                   │
│  2. Validate all addon_ids exist and are available                  │
│  3. Look up customer (if customer_id provided)                      │
│  4. Look up discount (if discount_id provided)                      │
│                                                                     │
│  5. Calculate pricing:                                              │
│     ┌─────────────────────────────────────────────────┐             │
│     │ For each item:                                   │             │
│     │   line_total = (item_price + Σ addon_prices)     │             │
│     │                 × quantity                        │             │
│     └─────────────────────────────────────────────────┘             │
│     subtotal    = Σ all line_totals                                 │
│     discount    = apply percentage or flat discount                  │
│     tax         = (subtotal - discount) × 0.08  (8%)               │
│     total       = subtotal - discount + tax                         │
│                                                                     │
│  6. Deduct stock for items with limited stock_qty                   │
│  7. Generate order number: PHI-YYYYMMDD-XXXX                       │
│  8. Set status = "pending"                                          │
│  9. Return full order with calculated totals                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Order Response Shape

```json
{
  "id": 442,
  "order_number": "PHI-20260302-0002",
  "customer_id": 2,
  "customer_name": "Bob Smith",
  "status": "pending",
  "payment_method": "cash",
  "subtotal": 6.75,
  "tax_amount": 0.54,
  "discount_amount": 0.0,
  "discount_id": null,
  "total": 7.29,
  "shift_id": null,
  "notes": null,
  "items": [
    {
      "id": 1102,
      "item_id": 5,
      "item_name": "Caramel Latte",
      "quantity": 1,
      "unit_price": 5.50,
      "subtotal": 6.75,
      "addons": [
        {
          "id": 490,
          "addon_id": 1,
          "addon_name": "Extra Espresso Shot",
          "price": 0.75
        },
        {
          "id": 491,
          "addon_id": 3,
          "addon_name": "Caramel Syrup",
          "price": 0.50
        }
      ]
    }
  ],
  "created_at": "2026-03-02T12:40:57",
  "updated_at": "2026-03-02T12:40:57"
}
```

### Updating Order Status

Send a `PATCH` to `/api/v1/orders/{id}/status`:

```json
{ "status": "preparing" }
```

---

## Order Lifecycle Diagram

```
                    ┌─────────┐
         ┌─────────│ PENDING │─────────┐
         │         └────┬────┘         │
         │              │              │
         │    PATCH     │              │ PATCH
         │ "cancelled"  │ "preparing"  │ "cancelled"
         │              │              │
         │              ▼              │
         │       ┌───────────┐         │
         │  ┌────│ PREPARING │─────┐   │
         │  │    └─────┬─────┘     │   │
         │  │          │           │   │
         │  │ PATCH    │ PATCH     │   │
         │  │"cancel"  │ "ready"   │   │
         │  │          │           │   │
         │  │          ▼           │   │
         │  │    ┌──────────┐      │   │
         │  │    │  READY   │──┐   │   │
         │  │    └────┬─────┘  │   │   │
         │  │         │        │   │   │
         │  │  PATCH  │ PATCH  │   │   │
         │  │"compltd"│"cancel"│   │   │
         │  │         │        │   │   │
         │  │         ▼        ▼   ▼   │
         │  │  ┌───────────┐ ┌──────────┐
         │  │  │ COMPLETED │ │CANCELLED │
         │  └──┤           │ │          │
         │     │   (final) │ │ (final)  │
         └─────►           │ │  stock   │
               │           │ │ restored │
               └───────────┘ └──────────┘
```

### Status Transition Rules

| Current Status | Allowed Next Status | Notes |
|---------------|-------------------|-------|
| `pending` | `preparing`, `cancelled` | Order just created |
| `preparing` | `ready`, `cancelled` | Kitchen is working on it |
| `ready` | `completed`, `cancelled` | Waiting for pickup |
| `completed` | — | **Final state.** Cannot change. |
| `cancelled` | — | **Final state.** Stock is restored. |

---

## 6. Discounts

> **Purpose**: Define reusable discounts (percentage or flat amount) that can be applied to orders.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/discounts` | List discounts |
| `POST` | `/api/v1/discounts` | Create a discount |
| `GET` | `/api/v1/discounts/{id}` | Get discount detail |
| `PATCH` | `/api/v1/discounts/{id}` | Update a discount |
| `DELETE` | `/api/v1/discounts/{id}` | Delete a discount |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `is_active` | bool | Only active/inactive discounts |
| `search` | string | Search in discount name |

### Create/Update Body

```json
{
  "name": "Happy Hour 20%",
  "type": "percentage",         // "percentage" or "flat"
  "value": 20.0,                // 20% off  OR  $20 off
  "is_active": true
}
```

### How Discounts Apply to Orders

```
┌─────────────────────────────────────────────┐
│  type: "percentage", value: 20              │
│  discount_amount = subtotal × (20 / 100)    │
│                                             │
│  type: "flat", value: 2.00                  │
│  discount_amount = min($2.00, subtotal)     │
└─────────────────────────────────────────────┘
```

**Pre-seeded discounts:** Happy Hour 20%, Student 10% Off, $2 Off Any Order, Weekend Special 15% (inactive)

---

## 7. Shifts

> **Purpose**: Track POS register sessions. A shift represents a work period with a starting and ending cash amount.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/v1/shifts/open` | Open a new shift |
| `GET` | `/api/v1/shifts` | List all shifts |
| `GET` | `/api/v1/shifts/{id}` | Get shift detail with totals |
| `PATCH` | `/api/v1/shifts/{id}/close` | Close an open shift |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `status` | string | `open` or `closed` |

### Open Shift Body

```json
{
  "opening_cash": 200.00,
  "notes": "Morning shift"
}
```

### Close Shift Body

```json
{
  "closing_cash": 485.50,
  "notes": "All good, no discrepancies"
}
```

### Response Shape

```json
{
  "id": 61,
  "opened_at": "2026-03-02T06:00:00",
  "closed_at": null,
  "opening_cash": 200.00,
  "closing_cash": null,
  "status": "open",
  "notes": "Morning shift",
  "total_orders": 12,
  "total_revenue": 245.80,
  "total_expenses": 45.00
}
```

> `total_orders`, `total_revenue`, and `total_expenses` are **computed automatically** from orders and expenses linked to that shift.

---

## Shift Lifecycle Diagram

```
                ┌──────────────────────┐
                │  POST /shifts/open   │
                │  opening_cash: 200   │
                └──────────┬───────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │         SHIFT: OPEN          │
            │                              │
            │  • Take orders (link via     │
            │    shift_id in POST /orders) │
            │  • Record expenses (link via │
            │    shift_id in POST/expenses)│
            │  • Only ONE shift can be     │
            │    open at a time            │
            │                              │
            └──────────────┬───────────────┘
                           │
                           ▼
           ┌───────────────────────────────┐
           │ PATCH /shifts/{id}/close      │
           │ closing_cash: 485.50          │
           └───────────────┬───────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │        SHIFT: CLOSED         │
            │                              │
            │  total_orders: 12            │
            │  total_revenue: 245.80       │
            │  total_expenses: 45.00       │
            │  cash_difference: computed   │
            └──────────────────────────────┘
```

> **Rule:** You **cannot** open a new shift if one is already open. Close the current shift first.

---

## 8. Expenses

> **Purpose**: Track business costs (supplies, wages, maintenance, etc.) per shift.

### Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/v1/expenses` | List expenses (filterable) |
| `POST` | `/api/v1/expenses` | Record a new expense |
| `GET` | `/api/v1/expenses/{id}` | Get expense detail |
| `PATCH` | `/api/v1/expenses/{id}` | Update an expense |
| `DELETE` | `/api/v1/expenses/{id}` | Delete an expense |

### Filters (GET list)

| Param | Type | Description |
|-------|------|-------------|
| `category` | string | Filter by category (e.g., `supplies`) |
| `shift_id` | int | Expenses for a specific shift |
| `start_date` | string | From date (`YYYY-MM-DD`) |
| `end_date` | string | To date (`YYYY-MM-DD`) |

### Create/Update Body

```json
{
  "category": "supplies",
  "description": "Coffee beans restocking",
  "amount": 150.00,
  "shift_id": 61           // optional
}
```

### Expense Categories

`supplies` · `maintenance` · `wages` · `utilities` · `marketing` · `rent` · `miscellaneous`

---

## 9. Dashboard Analytics

> **Purpose**: Rich analytics data for charts, KPIs, and business intelligence views.

All dashboard endpoints accept **optional date filters** to constrain the analysis period. If omitted, they default to the **last 30 days**.

### Date Filter Params (all dashboard endpoints)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `start_date` | string | 30 days ago | Start of period (`YYYY-MM-DD`) |
| `end_date` | string | today | End of period (`YYYY-MM-DD`) |

---

### 9.1 Summary KPIs

```
GET /api/v1/dashboard/summary
```

The **single most important dashboard call.** Returns all key performance indicators:

```json
{
  "total_revenue": 6977.52,
  "total_orders": 440,
  "completed_orders": 206,
  "cancelled_orders": 64,
  "avg_order_value": 18.56,
  "total_customers": 8,
  "new_customers": 8,
  "total_items_sold": 1237,
  "revenue_change_pct": 12.5,      // vs previous period
  "order_change_pct": 8.3,         // vs previous period
  "top_payment_method": "mobile",
  "busiest_hour": 9                // 0-23 (9 AM)
}
```

> `revenue_change_pct` and `order_change_pct` compare the selected period against the **equivalent previous period**. If you select 30 days, it compares to the 30 days before that.

---

### 9.2 Revenue Breakdown

```
GET /api/v1/dashboard/revenue?group_by=daily
```

| Extra Param | Values | Default |
|------------|--------|---------|
| `group_by` | `daily`, `weekly`, `monthly` | `daily` |

Returns time-series data for line/bar charts:

```json
[
  { "period": "2026-03-01", "revenue": 245.50, "order_count": 14, "avg_order_value": 17.54 },
  { "period": "2026-03-02", "revenue": 312.00, "order_count": 18, "avg_order_value": 17.33 }
]
```

---

### 9.3 Top Selling Items

```
GET /api/v1/dashboard/top-items?limit=10
```

| Extra Param | Default | Description |
|------------|---------|-------------|
| `limit` | `10` | Number of items to return (max 50) |

```json
[
  {
    "item_id": 5,
    "name": "Caramel Latte",
    "category": "Hot Coffee",
    "qty_sold": 64,
    "revenue": 372.50,
    "order_count": 44
  }
]
```

---

### 9.4 Top Categories

```
GET /api/v1/dashboard/top-categories?limit=10
```

```json
[
  {
    "category_id": 1,
    "name": "Hot Coffee",
    "item_count": 10,
    "total_revenue": 2450.00,
    "order_count": 180,
    "qty_sold": 520
  }
]
```

---

### 9.5 Order Trends

```
GET /api/v1/dashboard/order-trends?group_by=daily
```

```json
[
  {
    "date": "2026-03-01",
    "order_count": 14,
    "revenue": 245.50,
    "avg_order_value": 17.54,
    "completed": 10,
    "cancelled": 2
  }
]
```

---

### 9.6 Hourly Sales Heatmap

```
GET /api/v1/dashboard/hourly-heatmap
```

| Extra Param | Default | Description |
|------------|---------|-------------|
| `day_of_week` | all days | Filter single day (0=Sun, 6=Sat) |

Returns **24 data points** (one per hour, 0–23):

```json
[
  { "hour": 6, "order_count": 3, "revenue": 45.00, "avg_order_value": 15.00, "items_sold": 5 },
  { "hour": 7, "order_count": 8, "revenue": 120.50, "avg_order_value": 15.06, "items_sold": 14 },
  { "hour": 8, "order_count": 15, "revenue": 280.00, "avg_order_value": 18.67, "items_sold": 28 },
  // ... up to hour 23
]
```

> Perfect for a **heatmap grid** showing busy hours.

---

### 9.7 Customer Insights

```
GET /api/v1/dashboard/customer-insights?top_limit=10
```

| Extra Param | Default | Description |
|------------|---------|-------------|
| `top_limit` | `10` | Number of top customers to include |

```json
{
  "total_customers": 8,
  "active_customers": 6,
  "new_customers": 2,
  "repeat_customers": 4,
  "repeat_rate": 66.7,
  "avg_customer_spend": 85.30,
  "top_customers": [
    {
      "customer_id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "order_count": 15,
      "total_spent": 127.50,
      "avg_order_value": 8.50
    }
  ]
}
```

---

### 9.8 Payment Method Breakdown

```
GET /api/v1/dashboard/payment-breakdown
```

```json
[
  { "method": "mobile", "count": 141, "total_amount": 2619.94, "percentage": 37.5 },
  { "method": "card",   "count": 121, "total_amount": 2294.05, "percentage": 32.2 },
  { "method": "cash",   "count": 114, "total_amount": 2063.53, "percentage": 30.3 }
]
```

> Perfect for a **pie chart** or **donut chart**.

---

### 9.9 Inventory Alerts

```
GET /api/v1/dashboard/inventory-alerts
```

| Extra Param | Default | Description |
|------------|---------|-------------|
| `threshold` | `10` | Stock level threshold |

```json
[
  { "item_id": 29, "name": "Cinnamon Roll", "category": "Pastries & Bakery", "stock_qty": 3, "status": "low_stock" },
  { "item_id": 32, "name": "Turkey Panini", "category": "Snacks & Sandwiches", "stock_qty": 0, "status": "out_of_stock" }
]
```

> Only items with **tracked stock** appear (not items with `stock_qty: -1`).

---

### 9.10 Profit & Loss

```
GET /api/v1/dashboard/profit-loss
```

```json
{
  "total_revenue": 6977.52,
  "total_expenses": 8346.14,
  "gross_profit": -1368.62,
  "profit_margin": -19.61,
  "total_tax_collected": 517.04,
  "total_discounts_given": 99.02,
  "net_revenue": 6878.50,
  "expense_breakdown": [
    { "category": "supplies",     "amount": 1595.02, "percentage": 19.11 },
    { "category": "wages",        "amount": 839.17,  "percentage": 10.05 },
    { "category": "utilities",    "amount": 1013.66, "percentage": 12.15 },
    { "category": "rent",         "amount": 926.84,  "percentage": 11.11 },
    { "category": "maintenance",  "amount": 908.82,  "percentage": 10.89 },
    { "category": "marketing",    "amount": 1497.30, "percentage": 17.94 },
    { "category": "miscellaneous","amount": 1565.33, "percentage": 18.76 }
  ]
}
```

---

### 9.11 Shift Summary

```
GET /api/v1/dashboard/shift-summary
```

| Extra Param | Default | Description |
|------------|---------|-------------|
| `shift_id` | all shifts | Filter specific shift |

```json
[
  {
    "shift_id": 60,
    "opened_at": "2026-03-01T14:00:00",
    "closed_at": "2026-03-01T22:00:00",
    "status": "closed",
    "total_orders": 8,
    "total_revenue": 145.60,
    "total_expenses": 25.00,
    "net": 120.60,
    "opening_cash": 200.00,
    "closing_cash": 345.60,
    "cash_difference": 0.00
  }
]
```

---

## Data Relationship Map

This shows how all entities are connected:

```
┌──────────────┐       ┌──────────────┐
│  CATEGORIES  │──────<│    ITEMS     │
│              │ 1:N   │              │
│ id           │       │ id           │
│ name         │       │ category_id ─┤──── FK to categories
│ display_order│       │ name         │
│ is_active    │       │ price        │
└──────────────┘       │ stock_qty    │
                       │ is_available │
                       └──────┬───────┘
                              │
                              │ referenced in
                              ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  CUSTOMERS   │──────<│   ORDERS     │>──────│  DISCOUNTS   │
│  (optional)  │ 1:N   │              │ N:1   │              │
│ id           │       │ id           │       │ id           │
│ name         │       │ order_number │       │ name         │
│ phone        │       │ customer_id ─┤── FK  │ type         │
│ email        │       │ discount_id ─┤── FK  │ value        │
│ total_orders │       │ shift_id ────┤── FK  │ is_active    │
│ total_spent  │       │ status       │       └──────────────┘
└──────────────┘       │ payment_mthd │
                       │ subtotal     │       ┌──────────────┐
                       │ tax_amount   │>──────│   SHIFTS     │
                       │ discount_amt │ N:1   │              │
                       │ total        │       │ id           │
                       └──────┬───────┘       │ status       │
                              │               │ opening_cash │
                              │ 1:N           │ closing_cash │
                              ▼               └──────┬───────┘
                       ┌──────────────┐              │ 1:N
                       │ ORDER_ITEMS  │              ▼
                       │              │       ┌──────────────┐
                       │ id           │       │  EXPENSES    │
                       │ order_id ────┤── FK  │              │
                       │ item_id  ────┤── FK  │ id           │
                       │ quantity     │       │ shift_id ────┤── FK
                       │ unit_price   │       │ category     │
                       │ subtotal     │       │ amount       │
                       └──────┬───────┘       │ description  │
                              │               └──────────────┘
                              │ 1:N
                              ▼
                       ┌────────────────────┐      ┌──────────────┐
                       │ ORDER_ITEM_ADDONS  │>─────│   ADDONS     │
                       │                    │ N:1  │              │
                       │ id                 │      │ id           │
                       │ order_item_id ─────┤── FK │ name         │
                       │ addon_id ──────────┤── FK │ price        │
                       │ price              │      │ is_available │
                       └────────────────────┘      └──────────────┘
```

---

## Common Scenarios

### Scenario 1: Complete POS Transaction

```
1.  GET  /api/v1/categories                    → Display menu categories
2.  GET  /api/v1/items?category_id=1           → Show items in "Hot Coffee"
3.  GET  /api/v1/addons?is_available=true       → Show available add-ons
4.  GET  /api/v1/customers?search=Alice         → Find returning customer
5.  GET  /api/v1/discounts?is_active=true       → Show applicable discounts
6.  POST /api/v1/orders                         → Submit the order
7.  PATCH /api/v1/orders/{id}/status            → "preparing" (kitchen starts)
8.  PATCH /api/v1/orders/{id}/status            → "ready" (order is done)
9.  PATCH /api/v1/orders/{id}/status            → "completed" (handed to customer)
```

### Scenario 2: Start of Day

```
1.  POST /api/v1/shifts/open                    → Open register with starting cash
2.  GET  /api/v1/dashboard/summary              → See yesterday's KPIs
3.  GET  /api/v1/dashboard/inventory-alerts     → Check low stock items
```

### Scenario 3: End of Day

```
1.  PATCH /api/v1/shifts/{id}/close             → Close shift with ending cash
2.  GET   /api/v1/dashboard/profit-loss         → Review day's P&L
3.  GET   /api/v1/dashboard/shift-summary       → Verify shift numbers
4.  POST  /api/v1/expenses                      → Record any end-of-day expenses
```

### Scenario 4: Dashboard View

```
1.  GET /api/v1/dashboard/summary               → KPI cards at top
2.  GET /api/v1/dashboard/revenue?group_by=daily → Revenue line chart
3.  GET /api/v1/dashboard/top-items?limit=5      → Top items bar chart
4.  GET /api/v1/dashboard/hourly-heatmap         → Busy hours heatmap
5.  GET /api/v1/dashboard/payment-breakdown      → Payment pie chart
6.  GET /api/v1/dashboard/customer-insights      → Customer stats
7.  GET /api/v1/dashboard/order-trends           → Order volume chart
```

### Scenario 5: Walk-in Quick Order (No Customer)

```
POST /api/v1/orders
{
  "payment_method": "cash",
  "items": [
    { "item_id": 1, "quantity": 1, "addon_ids": [] }
  ]
}
```

> No `customer_id` needed. The response will show `customer_name: null`.

---

## Quick Reference: All Endpoints

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | `POST` | `/api/v1/categories` | Create category |
| 2 | `GET` | `/api/v1/categories` | List categories |
| 3 | `GET` | `/api/v1/categories/{id}` | Get category |
| 4 | `PATCH` | `/api/v1/categories/{id}` | Update category |
| 5 | `DELETE` | `/api/v1/categories/{id}` | Delete category |
| 6 | `POST` | `/api/v1/items` | Create item |
| 7 | `GET` | `/api/v1/items` | List items |
| 8 | `GET` | `/api/v1/items/{id}` | Get item |
| 9 | `PATCH` | `/api/v1/items/{id}` | Update item |
| 10 | `DELETE` | `/api/v1/items/{id}` | Delete item |
| 11 | `POST` | `/api/v1/addons` | Create add-on |
| 12 | `GET` | `/api/v1/addons` | List add-ons |
| 13 | `GET` | `/api/v1/addons/{id}` | Get add-on |
| 14 | `PATCH` | `/api/v1/addons/{id}` | Update add-on |
| 15 | `DELETE` | `/api/v1/addons/{id}` | Delete add-on |
| 16 | `POST` | `/api/v1/customers` | Create customer |
| 17 | `GET` | `/api/v1/customers` | List customers |
| 18 | `GET` | `/api/v1/customers/{id}` | Get customer |
| 19 | `GET` | `/api/v1/customers/{id}/orders` | Customer's orders |
| 20 | `PATCH` | `/api/v1/customers/{id}` | Update customer |
| 21 | `DELETE` | `/api/v1/customers/{id}` | Delete customer |
| 22 | `POST` | `/api/v1/orders` | Create order |
| 23 | `GET` | `/api/v1/orders` | List orders |
| 24 | `GET` | `/api/v1/orders/{id}` | Get order detail |
| 25 | `PATCH` | `/api/v1/orders/{id}/status` | Update status |
| 26 | `DELETE` | `/api/v1/orders/{id}` | Delete order |
| 27 | `POST` | `/api/v1/discounts` | Create discount |
| 28 | `GET` | `/api/v1/discounts` | List discounts |
| 29 | `GET` | `/api/v1/discounts/{id}` | Get discount |
| 30 | `PATCH` | `/api/v1/discounts/{id}` | Update discount |
| 31 | `DELETE` | `/api/v1/discounts/{id}` | Delete discount |
| 32 | `POST` | `/api/v1/shifts/open` | Open shift |
| 33 | `GET` | `/api/v1/shifts` | List shifts |
| 34 | `GET` | `/api/v1/shifts/{id}` | Get shift detail |
| 35 | `PATCH` | `/api/v1/shifts/{id}/close` | Close shift |
| 36 | `POST` | `/api/v1/expenses` | Create expense |
| 37 | `GET` | `/api/v1/expenses` | List expenses |
| 38 | `GET` | `/api/v1/expenses/{id}` | Get expense |
| 39 | `PATCH` | `/api/v1/expenses/{id}` | Update expense |
| 40 | `DELETE` | `/api/v1/expenses/{id}` | Delete expense |
| 41 | `GET` | `/api/v1/dashboard/summary` | KPI summary |
| 42 | `GET` | `/api/v1/dashboard/revenue` | Revenue breakdown |
| 43 | `GET` | `/api/v1/dashboard/top-items` | Top selling items |
| 44 | `GET` | `/api/v1/dashboard/top-categories` | Top categories |
| 45 | `GET` | `/api/v1/dashboard/order-trends` | Order trends |
| 46 | `GET` | `/api/v1/dashboard/hourly-heatmap` | Hourly heatmap |
| 47 | `GET` | `/api/v1/dashboard/customer-insights` | Customer analytics |
| 48 | `GET` | `/api/v1/dashboard/payment-breakdown` | Payment methods |
| 49 | `GET` | `/api/v1/dashboard/inventory-alerts` | Low stock alerts |
| 50 | `GET` | `/api/v1/dashboard/profit-loss` | P&L statement |
| 51 | `GET` | `/api/v1/dashboard/shift-summary` | Shift performance |

---

> **Tip:** Open `http://localhost:8000/docs` to try every endpoint interactively with Swagger UI. The database comes **pre-seeded** with 37 menu items, 12 add-ons, 8 customers, 440 orders, and full 30-day analytics data — you can start building the frontend immediately.
