API Endpoints
=============

All endpoints are prefixed with ``/api/v1`` unless otherwise specified. The API uses JSON for request and response bodies.

Base URL: ``http://localhost:8000``

----

Health Check
------------

**GET /health**

Health-check endpoint for monitoring.

.. code-block:: bash

   curl -X GET http://localhost:8000/health

**Response (200):**

.. code-block:: json

   {
     "status": "healthy",
     "app": "Philo Coffee Shop",
     "version": "1.0.0"
   }

----

Categories
----------

Create Category
~~~~~~~~~~~~~~~

**POST /api/v1/categories**

Create a new menu category.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/categories \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Hot Beverages",
       "description": "Coffee, tea, and hot drinks",
       "display_order": 1,
       "is_active": true
     }'

**Request Body:**

.. code-block:: json

   {
     "name": "Hot Beverages",
     "description": "Coffee, tea, and hot drinks",
     "display_order": 1,
     "is_active": true
   }

**Fields:**

- ``name`` (string, required): Category name, 1-100 characters
- ``description`` (string, optional): Category description
- ``display_order`` (int, optional): Display order, >= 0, default: 0
- ``is_active`` (bool, optional): Active status, default: true

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "name": "Hot Beverages",
     "description": "Coffee, tea, and hot drinks",
     "display_order": 1,
     "is_active": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Categories
~~~~~~~~~~~~~~~

**GET /api/v1/categories**

Get paginated list of categories with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/categories?page=1&per_page=20&is_active=true"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``is_active`` (bool, optional): Filter by active status
- ``search`` (string, optional): Search in category name

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "name": "Hot Beverages",
         "description": "Coffee, tea, and hot drinks",
         "display_order": 1,
         "is_active": true,
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 42,
     "page": 1,
     "per_page": 20,
     "total_pages": 3
   }

Get Category by ID
~~~~~~~~~~~~~~~~~~

**GET /api/v1/categories/{category_id}**

Get a single category by its ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/categories/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Hot Beverages",
     "description": "Coffee, tea, and hot drinks",
     "display_order": 1,
     "is_active": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Category
~~~~~~~~~~~~~~~

**PATCH /api/v1/categories/{category_id}**

Update an existing category (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/categories/1 \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Hot Drinks",
       "is_active": true
     }'

**Request Body:**

.. code-block:: json

   {
     "name": "Hot Drinks",
     "display_order": 2,
     "is_active": true
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Hot Drinks",
     "description": "Coffee, tea, and hot drinks",
     "display_order": 2,
     "is_active": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T11:00:00Z"
   }

Delete Category
~~~~~~~~~~~~~~~

**DELETE /api/v1/categories/{category_id}**

Delete a category (fails if category has items).

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/categories/1

**Response (200):**

.. code-block:: json

   {
     "message": "Category deleted successfully"
   }

----

Items
-----

Create Item
~~~~~~~~~~~

**POST /api/v1/items**

Create a new menu item.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/items \
     -H "Content-Type: application/json" \
     -d '{
       "category_id": 1,
       "name": "Cappuccino",
       "description": "Espresso with steamed milk foam",
       "price": 4.50,
       "image_url": "https://example.com/cappuccino.jpg",
       "is_available": true,
       "stock_qty": -1
     }'

**Request Body:**

.. code-block:: json

   {
     "category_id": 1,
     "name": "Cappuccino",
     "description": "Espresso with steamed milk foam",
     "price": 4.50,
     "image_url": "https://example.com/cappuccino.jpg",
     "is_available": true,
     "stock_qty": -1
   }

**Fields:**

- ``category_id`` (int, required): Category ID, > 0
- ``name`` (string, required): Item name, 1-200 characters
- ``description`` (string, optional): Item description
- ``price`` (float, required): Price, > 0
- ``image_url`` (string, optional): Image URL, max 500 characters
- ``is_available`` (bool, optional): Availability, default: true
- ``stock_qty`` (int, optional): Stock quantity, >= -1, default: -1 (-1 = unlimited)

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "category_id": 1,
     "name": "Cappuccino",
     "description": "Espresso with steamed milk foam",
     "price": 4.50,
     "image_url": "https://example.com/cappuccino.jpg",
     "is_available": true,
     "stock_qty": -1,
     "category": {
       "id": 1,
       "name": "Hot Beverages"
     },
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Items
~~~~~~~~~~

**GET /api/v1/items**

Get paginated list of items with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/items?page=1&per_page=20&category_id=1&is_available=true&min_price=3.00&max_price=10.00"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``category_id`` (int, optional): Filter by category
- ``is_available`` (bool, optional): Filter by availability
- ``search`` (string, optional): Search in name/description
- ``min_price`` (float, optional): Minimum price, >= 0
- ``max_price`` (float, optional): Maximum price, >= 0

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "category_id": 1,
         "name": "Cappuccino",
         "description": "Espresso with steamed milk foam",
         "price": 4.50,
         "image_url": "https://example.com/cappuccino.jpg",
         "is_available": true,
         "stock_qty": -1,
         "category": {
           "id": 1,
           "name": "Hot Beverages"
         },
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 37,
     "page": 1,
     "per_page": 20,
     "total_pages": 2
   }

Get Item by ID
~~~~~~~~~~~~~~

**GET /api/v1/items/{item_id}**

Get a single item by its ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/items/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "category_id": 1,
     "name": "Cappuccino",
     "description": "Espresso with steamed milk foam",
     "price": 4.50,
     "image_url": "https://example.com/cappuccino.jpg",
     "is_available": true,
     "stock_qty": -1,
     "category": {
       "id": 1,
       "name": "Hot Beverages"
     },
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Item
~~~~~~~~~~~

**PATCH /api/v1/items/{item_id}**

Update an existing item (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/items/1 \
     -H "Content-Type: application/json" \
     -d '{
       "price": 4.75,
       "is_available": true
     }'

**Request Body:**

.. code-block:: json

   {
     "price": 4.75,
     "is_available": true,
     "stock_qty": 50
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "category_id": 1,
     "name": "Cappuccino",
     "description": "Espresso with steamed milk foam",
     "price": 4.75,
     "image_url": "https://example.com/cappuccino.jpg",
     "is_available": true,
     "stock_qty": 50,
     "category": {
       "id": 1,
       "name": "Hot Beverages"
     },
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T11:30:00Z"
   }

Delete Item
~~~~~~~~~~~

**DELETE /api/v1/items/{item_id}**

Delete a menu item.

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/items/1

**Response (200):**

.. code-block:: json

   {
     "message": "Item deleted successfully"
   }

----

Addons
------

Create Addon
~~~~~~~~~~~~

**POST /api/v1/addons**

Create a new addon/extra option.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/addons \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Extra Shot",
       "price": 0.75,
       "is_available": true
     }'

**Request Body:**

.. code-block:: json

   {
     "name": "Extra Shot",
     "price": 0.75,
     "is_available": true
   }

**Fields:**

- ``name`` (string, required): Addon name, 1-100 characters
- ``price`` (float, required): Price, >= 0
- ``is_available`` (bool, optional): Availability, default: true

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "name": "Extra Shot",
     "price": 0.75,
     "is_available": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Addons
~~~~~~~~~~~

**GET /api/v1/addons**

Get paginated list of addons with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/addons?page=1&per_page=20&is_available=true"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``is_available`` (bool, optional): Filter by availability
- ``search`` (string, optional): Search in addon name

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "name": "Extra Shot",
         "price": 0.75,
         "is_available": true,
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 12,
     "page": 1,
     "per_page": 20,
     "total_pages": 1
   }

Get Addon by ID
~~~~~~~~~~~~~~~

**GET /api/v1/addons/{addon_id}**

Get a single addon by its ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/addons/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Extra Shot",
     "price": 0.75,
     "is_available": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Addon
~~~~~~~~~~~~

**PATCH /api/v1/addons/{addon_id}**

Update an existing addon (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/addons/1 \
     -H "Content-Type: application/json" \
     -d '{
       "price": 1.00,
       "is_available": true
     }'

**Request Body:**

.. code-block:: json

   {
     "price": 1.00,
     "is_available": true
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Extra Shot",
     "price": 1.00,
     "is_available": true,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T11:00:00Z"
   }

Delete Addon
~~~~~~~~~~~~

**DELETE /api/v1/addons/{addon_id}**

Delete an addon.

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/addons/1

**Response (200):**

.. code-block:: json

   {
     "message": "Addon deleted successfully"
   }

----

Customers
---------

Create Customer
~~~~~~~~~~~~~~~

**POST /api/v1/customers**

Register a new customer.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/customers \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Johnson",
       "phone": "+1234567890",
       "email": "alice@example.com"
     }'

**Request Body:**

.. code-block:: json

   {
     "name": "Alice Johnson",
     "phone": "+1234567890",
     "email": "alice@example.com"
   }

**Fields:**

- ``name`` (string, required): Customer name, 1-200 characters
- ``phone`` (string, optional): Phone number, max 20 characters, unique
- ``email`` (string, optional): Email address, max 200 characters, unique

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "name": "Alice Johnson",
     "phone": "+1234567890",
     "email": "alice@example.com",
     "total_orders": 0,
     "total_spent": 0.0,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Customers
~~~~~~~~~~~~~~

**GET /api/v1/customers**

Get paginated list of customers with optional search.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/customers?page=1&per_page=20&search=alice"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``search`` (string, optional): Search by name, phone, or email

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "name": "Alice Johnson",
         "phone": "+1234567890",
         "email": "alice@example.com",
         "total_orders": 15,
         "total_spent": 127.50,
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 8,
     "page": 1,
     "per_page": 20,
     "total_pages": 1
   }

Get Customer by ID
~~~~~~~~~~~~~~~~~~

**GET /api/v1/customers/{customer_id}**

Get a single customer by their ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/customers/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Alice Johnson",
     "phone": "+1234567890",
     "email": "alice@example.com",
     "total_orders": 15,
     "total_spent": 127.50,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Get Customer Orders
~~~~~~~~~~~~~~~~~~~

**GET /api/v1/customers/{customer_id}/orders**

Get all orders for a specific customer.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/customers/1/orders

**Response (200):**

.. code-block:: json

   [
     {
       "id": 1,
       "order_number": "PHI-20250115-0001",
       "status": "completed",
       "payment_method": "card",
       "subtotal": 12.00,
       "tax_amount": 0.96,
       "discount_amount": 0.0,
       "total": 12.96,
       "customer_id": 1,
       "shift_id": 1,
       "notes": null,
       "created_at": "2026-01-15T10:30:00Z",
       "updated_at": "2026-01-15T10:45:00Z"
     }
   ]

Update Customer
~~~~~~~~~~~~~~~

**PATCH /api/v1/customers/{customer_id}**

Update an existing customer (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/customers/1 \
     -H "Content-Type: application/json" \
     -d '{
       "phone": "+1987654321"
     }'

**Request Body:**

.. code-block:: json

   {
     "phone": "+1987654321",
     "email": "alice.j@example.com"
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Alice Johnson",
     "phone": "+1987654321",
     "email": "alice.j@example.com",
     "total_orders": 15,
     "total_spent": 127.50,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T12:00:00Z"
   }

Delete Customer
~~~~~~~~~~~~~~~

**DELETE /api/v1/customers/{customer_id}**

Delete a customer record.

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/customers/1

**Response (200):**

.. code-block:: json

   {
     "message": "Customer deleted successfully"
   }

----

Discounts
---------

Create Discount
~~~~~~~~~~~~~~~

**POST /api/v1/discounts**

Create a new discount/promotion.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/discounts \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Happy Hour 20% Off",
       "type": "percentage",
       "value": 20.0,
       "is_active": true,
       "start_date": "2026-01-15T14:00:00Z",
       "end_date": "2026-01-15T17:00:00Z"
     }'

**Request Body:**

.. code-block:: json

   {
     "name": "Happy Hour 20% Off",
     "type": "percentage",
     "value": 20.0,
     "is_active": true,
     "start_date": "2026-01-15T14:00:00Z",
     "end_date": "2026-01-15T17:00:00Z"
   }

**Fields:**

- ``name`` (string, required): Discount name, 1-200 characters
- ``type`` (string, required): "percentage" or "flat", default: "percentage"
- ``value`` (float, required): 0-100 for percentage, dollar amount for flat, > 0
- ``is_active`` (bool, optional): Active status, default: true
- ``start_date`` (datetime, optional): Start date/time
- ``end_date`` (datetime, optional): End date/time

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "name": "Happy Hour 20% Off",
     "type": "percentage",
     "value": 20.0,
     "is_active": true,
     "start_date": "2026-01-15T14:00:00Z",
     "end_date": "2026-01-15T17:00:00Z",
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Discounts
~~~~~~~~~~~~~~

**GET /api/v1/discounts**

Get paginated list of discounts with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/discounts?page=1&per_page=20&is_active=true"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``is_active`` (bool, optional): Filter by active status
- ``search`` (string, optional): Search in discount name

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "name": "Happy Hour 20% Off",
         "type": "percentage",
         "value": 20.0,
         "is_active": true,
         "start_date": "2026-01-15T14:00:00Z",
         "end_date": "2026-01-15T17:00:00Z",
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 4,
     "page": 1,
     "per_page": 20,
     "total_pages": 1
   }

Get Discount by ID
~~~~~~~~~~~~~~~~~~

**GET /api/v1/discounts/{discount_id}**

Get a single discount by its ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/discounts/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Happy Hour 20% Off",
     "type": "percentage",
     "value": 20.0,
     "is_active": true,
     "start_date": "2026-01-15T14:00:00Z",
     "end_date": "2026-01-15T17:00:00Z",
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Discount
~~~~~~~~~~~~~~~

**PATCH /api/v1/discounts/{discount_id}**

Update an existing discount (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/discounts/1 \
     -H "Content-Type: application/json" \
     -d '{
       "value": 25.0,
       "is_active": true
     }'

**Request Body:**

.. code-block:: json

   {
     "value": 25.0,
     "is_active": true
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "name": "Happy Hour 20% Off",
     "type": "percentage",
     "value": 25.0,
     "is_active": true,
     "start_date": "2026-01-15T14:00:00Z",
     "end_date": "2026-01-15T17:00:00Z",
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T11:00:00Z"
   }

Delete Discount
~~~~~~~~~~~~~~~

**DELETE /api/v1/discounts/{discount_id}**

Delete a discount.

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/discounts/1

**Response (200):**

.. code-block:: json

   {
     "message": "Discount deleted successfully"
   }

----

Orders
------

Create Order
~~~~~~~~~~~~

**POST /api/v1/orders**

Create a new order with line items and addons. Auto-calculates subtotal, tax, discount, and total. Deducts stock for limited items. Order number auto-generated as PHI-YYYYMMDD-XXXX.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/orders \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": 1,
       "payment_method": "card",
       "discount_id": null,
       "shift_id": 1,
       "notes": "Extra hot",
       "items": [
         {
           "item_id": 1,
           "quantity": 2,
           "addon_ids": [1, 3]
         },
         {
           "item_id": 5,
           "quantity": 1,
           "addons": [
             {"addon_id": 2}
           ]
         }
       ]
     }'

**Request Body:**

.. code-block:: json

   {
     "customer_id": 1,
     "payment_method": "card",
     "discount_id": null,
     "shift_id": 1,
     "notes": "Extra hot",
     "items": [
       {
         "item_id": 1,
         "quantity": 2,
         "addon_ids": [1, 3]
       },
       {
         "item_id": 5,
         "quantity": 1,
         "addons": [
           {"addon_id": 2}
         ]
       }
     ]
   }

**Fields:**

- ``customer_id`` (int, optional): Customer ID, > 0, null for walk-in
- ``payment_method`` (string, required): "cash", "card", or "mobile", default: "cash"
- ``discount_id`` (int, optional): Discount ID, > 0
- ``shift_id`` (int, optional): Shift ID, > 0
- ``notes`` (string, optional): Order notes
- ``items`` (array, required): Order items, minimum 1 item

  - ``item_id`` (int, required): Item ID, > 0
  - ``quantity`` (int, optional): Quantity, 1-100, default: 1
  - ``addon_ids`` (array, optional): Addon IDs shorthand
  - ``addons`` (array, optional): Addons detail

    - ``addon_id`` (int, required): Addon ID, > 0

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "order_number": "PHI-20250115-0001",
     "status": "pending",
     "payment_method": "card",
     "subtotal": 17.25,
     "tax_amount": 1.38,
     "discount_amount": 0.0,
     "total": 18.63,
     "customer_id": 1,
     "customer": {
       "id": 1,
       "name": "Alice Johnson"
     },
     "shift_id": 1,
     "discount_id": null,
     "notes": "Extra hot",
     "items": [
       {
         "id": 1,
         "item_id": 1,
         "item_name": "Cappuccino",
         "quantity": 2,
         "unit_price": 4.50,
         "subtotal": 9.00,
         "addons": [
           {
             "id": 1,
             "addon_id": 1,
             "addon_name": "Extra Shot",
             "price": 0.75
           },
           {
             "id": 2,
             "addon_id": 3,
             "addon_name": "Oat Milk",
             "price": 0.50
           }
         ]
       },
       {
         "id": 2,
         "item_id": 5,
         "item_name": "Latte",
         "quantity": 1,
         "unit_price": 5.00,
         "subtotal": 5.00,
         "addons": [
           {
             "id": 3,
             "addon_id": 2,
             "addon_name": "Vanilla Syrup",
             "price": 0.50
           }
         ]
       }
     ],
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Orders
~~~~~~~~~~~

**GET /api/v1/orders**

Get paginated list of orders with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/orders?page=1&per_page=20&status=pending&payment_method=card&start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``status`` (string, optional): Filter by status: "pending", "preparing", "ready", "completed", "cancelled"
- ``payment_method`` (string, optional): Filter by: "cash", "card", "mobile"
- ``customer_id`` (int, optional): Filter by customer ID
- ``shift_id`` (int, optional): Filter by shift ID
- ``start_date`` (string, optional): Filter from date, format: YYYY-MM-DD
- ``end_date`` (string, optional): Filter to date, format: YYYY-MM-DD

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "order_number": "PHI-20250115-0001",
         "status": "pending",
         "payment_method": "card",
         "subtotal": 17.25,
         "tax_amount": 1.38,
         "discount_amount": 0.0,
         "total": 18.63,
         "customer_id": 1,
         "customer": {
           "id": 1,
           "name": "Alice Johnson"
         },
         "shift_id": 1,
         "discount_id": null,
         "notes": "Extra hot",
         "items": [],
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 440,
     "page": 1,
     "per_page": 20,
     "total_pages": 22
   }

Get Order by ID
~~~~~~~~~~~~~~~

**GET /api/v1/orders/{order_id}**

Get a single order by its ID with all line items and addons.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/orders/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "order_number": "PHI-20250115-0001",
     "status": "pending",
     "payment_method": "card",
     "subtotal": 17.25,
     "tax_amount": 1.38,
     "discount_amount": 0.0,
     "total": 18.63,
     "customer_id": 1,
     "customer": {
       "id": 1,
       "name": "Alice Johnson"
     },
     "shift_id": 1,
     "discount_id": null,
     "notes": "Extra hot",
     "items": [
       {
         "id": 1,
         "item_id": 1,
         "item_name": "Cappuccino",
         "quantity": 2,
         "unit_price": 4.50,
         "subtotal": 9.00,
         "addons": [
           {
             "id": 1,
             "addon_id": 1,
             "addon_name": "Extra Shot",
             "price": 0.75
           }
         ]
       }
     ],
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Order Status
~~~~~~~~~~~~~~~~~~~

**PATCH /api/v1/orders/{order_id}/status**

Update order status with validation. Valid transitions: pending → preparing/cancelled, preparing → ready/cancelled, ready → completed/cancelled. Cancelling restores stock.

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/orders/1/status \
     -H "Content-Type: application/json" \
     -d '{
       "status": "preparing"
     }'

**Request Body:**

.. code-block:: json

   {
     "status": "preparing"
   }

**Fields:**

- ``status`` (string, required): "pending", "preparing", "ready", "completed", or "cancelled"

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "order_number": "PHI-20250115-0001",
     "status": "preparing",
     "payment_method": "card",
     "subtotal": 17.25,
     "tax_amount": 1.38,
     "discount_amount": 0.0,
     "total": 18.63,
     "customer_id": 1,
     "shift_id": 1,
     "notes": "Extra hot",
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:35:00Z"
   }

Delete Order
~~~~~~~~~~~~

**DELETE /api/v1/orders/{order_id}**

Delete an order (cannot delete completed orders).

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/orders/1

**Response (200):**

.. code-block:: json

   {
     "message": "Order deleted successfully"
   }

----

Shifts
------

Open Shift
~~~~~~~~~~

**POST /api/v1/shifts/open**

Open a new cashier shift. Only one shift can be open at a time.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/shifts/open \
     -H "Content-Type: application/json" \
     -d '{
       "opening_cash": 200.0,
       "notes": "Morning shift"
     }'

**Request Body:**

.. code-block:: json

   {
     "opening_cash": 200.0,
     "notes": "Morning shift"
   }

**Fields:**

- ``opening_cash`` (float, optional): Opening cash amount, >= 0, default: 0.0
- ``notes`` (string, optional): Shift notes

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "opened_at": "2026-01-15T08:00:00Z",
     "closed_at": null,
     "status": "open",
     "opening_cash": 200.0,
     "closing_cash": null,
     "cash_difference": null,
     "total_orders": 0,
     "total_revenue": 0.0,
     "total_expenses": 0.0,
     "notes": "Morning shift",
     "created_at": "2026-01-15T08:00:00Z",
     "updated_at": "2026-01-15T08:00:00Z"
   }

List Shifts
~~~~~~~~~~~

**GET /api/v1/shifts**

Get paginated list of shifts with optional status filter.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/shifts?page=1&per_page=20&status=open"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``status`` (string, optional): Filter by: "open" or "closed"

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "opened_at": "2026-01-15T08:00:00Z",
         "closed_at": null,
         "status": "open",
         "opening_cash": 200.0,
         "closing_cash": null,
         "cash_difference": null,
         "total_orders": 15,
         "total_revenue": 287.50,
         "total_expenses": 45.00,
         "notes": "Morning shift",
         "created_at": "2026-01-15T08:00:00Z",
         "updated_at": "2026-01-15T08:00:00Z"
       }
     ],
     "total": 61,
     "page": 1,
     "per_page": 20,
     "total_pages": 4
   }

Get Shift by ID
~~~~~~~~~~~~~~~

**GET /api/v1/shifts/{shift_id}**

Get a single shift by its ID with order and expense summaries.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/shifts/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "opened_at": "2026-01-15T08:00:00Z",
     "closed_at": null,
     "status": "open",
     "opening_cash": 200.0,
     "closing_cash": null,
     "cash_difference": null,
     "total_orders": 15,
     "total_revenue": 287.50,
     "total_expenses": 45.00,
     "notes": "Morning shift",
     "created_at": "2026-01-15T08:00:00Z",
     "updated_at": "2026-01-15T08:00:00Z"
   }

Close Shift
~~~~~~~~~~~

**PATCH /api/v1/shifts/{shift_id}/close**

Close an open shift.

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/shifts/1/close \
     -H "Content-Type: application/json" \
     -d '{
       "closing_cash": 485.50,
       "notes": "End of shift - balanced"
     }'

**Request Body:**

.. code-block:: json

   {
     "closing_cash": 485.50,
     "notes": "End of shift - balanced"
   }

**Fields:**

- ``closing_cash`` (float, required): Closing cash amount, >= 0
- ``notes`` (string, optional): Closing notes

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "opened_at": "2026-01-15T08:00:00Z",
     "closed_at": "2026-01-15T16:00:00Z",
     "status": "closed",
     "opening_cash": 200.0,
     "closing_cash": 485.50,
     "cash_difference": 0.0,
     "total_orders": 42,
     "total_revenue": 765.50,
     "total_expenses": 120.00,
     "notes": "End of shift - balanced",
     "created_at": "2026-01-15T08:00:00Z",
     "updated_at": "2026-01-15T16:00:00Z"
   }

----

Expenses
--------

Create Expense
~~~~~~~~~~~~~~

**POST /api/v1/expenses**

Record a new business expense.

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/expenses \
     -H "Content-Type: application/json" \
     -d '{
       "category": "supplies",
       "description": "Coffee beans - 10kg",
       "amount": 85.00,
       "date": "2026-01-15T10:30:00Z",
       "shift_id": 1
     }'

**Request Body:**

.. code-block:: json

   {
     "category": "supplies",
     "description": "Coffee beans - 10kg",
     "amount": 85.00,
     "date": "2026-01-15T10:30:00Z",
     "shift_id": 1
   }

**Fields:**

- ``category`` (string, required): Expense category, 1-100 characters (e.g., 'supplies', 'maintenance', 'wages', 'utilities')
- ``description`` (string, optional): Expense description
- ``amount`` (float, required): Amount, > 0
- ``date`` (datetime, optional): Expense date/time, defaults to now
- ``shift_id`` (int, optional): Shift ID, > 0

**Response (201):**

.. code-block:: json

   {
     "id": 1,
     "category": "supplies",
     "description": "Coffee beans - 10kg",
     "amount": 85.00,
     "date": "2026-01-15T10:30:00Z",
     "shift_id": 1,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

List Expenses
~~~~~~~~~~~~~

**GET /api/v1/expenses**

Get paginated list of expenses with optional filters.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/expenses?page=1&per_page=20&category=supplies&start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``page`` (int, optional): Page number, >= 1, default: 1
- ``per_page`` (int, optional): Items per page, 1-100, default: 20
- ``category`` (string, optional): Filter by expense category
- ``shift_id`` (int, optional): Filter by shift ID
- ``start_date`` (string, optional): Filter from date, format: YYYY-MM-DD
- ``end_date`` (string, optional): Filter to date, format: YYYY-MM-DD

**Response (200):**

.. code-block:: json

   {
     "items": [
       {
         "id": 1,
         "category": "supplies",
         "description": "Coffee beans - 10kg",
         "amount": 85.00,
         "date": "2026-01-15T10:30:00Z",
         "shift_id": 1,
         "created_at": "2026-01-15T10:30:00Z",
         "updated_at": "2026-01-15T10:30:00Z"
       }
     ],
     "total": 64,
     "page": 1,
     "per_page": 20,
     "total_pages": 4
   }

Get Expense by ID
~~~~~~~~~~~~~~~~~

**GET /api/v1/expenses/{expense_id}**

Get a single expense by its ID.

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/expenses/1

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "category": "supplies",
     "description": "Coffee beans - 10kg",
     "amount": 85.00,
     "date": "2026-01-15T10:30:00Z",
     "shift_id": 1,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T10:30:00Z"
   }

Update Expense
~~~~~~~~~~~~~~

**PATCH /api/v1/expenses/{expense_id}**

Update an existing expense (only provided fields are updated).

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/expenses/1 \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 90.00,
       "description": "Coffee beans - 10kg (premium)"
     }'

**Request Body:**

.. code-block:: json

   {
     "amount": 90.00,
     "description": "Coffee beans - 10kg (premium)"
   }

**Response (200):**

.. code-block:: json

   {
     "id": 1,
     "category": "supplies",
     "description": "Coffee beans - 10kg (premium)",
     "amount": 90.00,
     "date": "2026-01-15T10:30:00Z",
     "shift_id": 1,
     "created_at": "2026-01-15T10:30:00Z",
     "updated_at": "2026-01-15T11:00:00Z"
   }

Delete Expense
~~~~~~~~~~~~~~

**DELETE /api/v1/expenses/{expense_id}**

Delete an expense record.

.. code-block:: bash

   curl -X DELETE http://localhost:8000/api/v1/expenses/1

**Response (200):**

.. code-block:: json

   {
     "message": "Expense deleted successfully"
   }

----

Dashboard
---------

Dashboard Summary
~~~~~~~~~~~~~~~~~

**GET /api/v1/dashboard/summary**

Get overall dashboard KPI summary with period-over-period comparison.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/summary?start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD, default: 30 days ago
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD, default: today

**Response (200):**

.. code-block:: json

   {
     "total_revenue": 15234.50,
     "total_orders": 342,
     "completed_orders": 320,
     "cancelled_orders": 22,
     "avg_order_value": 44.56,
     "total_customers": 125,
     "new_customers": 18,
     "total_items_sold": 856,
     "revenue_change_pct": 12.5,
     "order_change_pct": 8.3,
     "top_payment_method": "card",
     "busiest_hour": 14
   }

Revenue Breakdown
~~~~~~~~~~~~~~~~~

**GET /api/v1/dashboard/revenue**

Get revenue breakdown grouped by time period.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/revenue?start_date=2026-01-01&end_date=2026-01-31&group_by=daily"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``group_by`` (string, optional): "daily", "weekly", or "monthly", default: "daily"

**Response (200):**

.. code-block:: json

   [
     {
       "period": "2026-01-15",
       "revenue": 765.50,
       "order_count": 42,
       "avg_order_value": 18.23
     },
     {
       "period": "2026-01-16",
       "revenue": 892.30,
       "order_count": 51,
       "avg_order_value": 17.50
     }
   ]

Top Items
~~~~~~~~~

**GET /api/v1/dashboard/top-items**

Get top-selling menu items ranked by quantity sold.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/top-items?start_date=2026-01-01&end_date=2026-01-31&limit=10"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``limit`` (int, optional): Maximum results, 1-50, default: 10

**Response (200):**

.. code-block:: json

   [
     {
       "item_id": 1,
       "name": "Cappuccino",
       "category": "Hot Beverages",
       "qty_sold": 156,
       "revenue": 702.00,
       "order_count": 98
     },
     {
       "item_id": 5,
       "name": "Latte",
       "category": "Hot Beverages",
       "qty_sold": 142,
       "revenue": 710.00,
       "order_count": 89
     }
   ]

Top Categories
~~~~~~~~~~~~~~

**GET /api/v1/dashboard/top-categories**

Get top-performing categories ranked by revenue.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/top-categories?start_date=2026-01-01&end_date=2026-01-31&limit=10"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``limit`` (int, optional): Maximum results, 1-50, default: 10

**Response (200):**

.. code-block:: json

   [
     {
       "category_id": 1,
       "name": "Hot Beverages",
       "item_count": 12,
       "total_revenue": 8542.50,
       "order_count": 425,
       "qty_sold": 752
     },
     {
       "category_id": 2,
       "name": "Pastries",
       "item_count": 8,
       "total_revenue": 4320.00,
       "order_count": 318,
       "qty_sold": 524
     }
   ]

Order Trends
~~~~~~~~~~~~

**GET /api/v1/dashboard/order-trends**

Get order volume and revenue trends over time.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/order-trends?start_date=2026-01-01&end_date=2026-01-31&group_by=daily"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``group_by`` (string, optional): "daily", "weekly", or "monthly", default: "daily"

**Response (200):**

.. code-block:: json

   [
     {
       "date": "2026-01-15",
       "order_count": 42,
       "revenue": 765.50,
       "avg_order_value": 18.23,
       "completed": 40,
       "cancelled": 2
     },
     {
       "date": "2026-01-16",
       "order_count": 51,
       "revenue": 892.30,
       "avg_order_value": 17.50,
       "completed": 49,
       "cancelled": 2
     }
   ]

Hourly Heatmap
~~~~~~~~~~~~~~

**GET /api/v1/dashboard/hourly-heatmap**

Get hourly sales distribution for heatmap visualization (24 data points).

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/hourly-heatmap?start_date=2026-01-01&end_date=2026-01-31&day_of_week=1"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``day_of_week`` (int, optional): Day of week, 0-6 (0=Sunday, 6=Saturday)

**Response (200):**

.. code-block:: json

   [
     {
       "hour": 8,
       "order_count": 12,
       "revenue": 145.50,
       "avg_order_value": 12.13,
       "items_sold": 28
     },
     {
       "hour": 9,
       "order_count": 24,
       "revenue": 287.30,
       "avg_order_value": 11.97,
       "items_sold": 52
     }
   ]

Customer Insights
~~~~~~~~~~~~~~~~~

**GET /api/v1/dashboard/customer-insights**

Get customer analytics including top customers and repeat rate.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/customer-insights?start_date=2026-01-01&end_date=2026-01-31&top_limit=10"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD
- ``top_limit`` (int, optional): Top customers to return, 1-50, default: 10

**Response (200):**

.. code-block:: json

   {
     "total_customers": 125,
     "active_customers": 98,
     "new_customers": 18,
     "repeat_customers": 65,
     "repeat_rate": 52.0,
     "avg_customer_spend": 121.88,
     "top_customers": [
       {
         "customer_id": 1,
         "name": "Alice Johnson",
         "order_count": 28,
         "total_spent": 487.50,
         "avg_order_value": 17.41
       },
       {
         "customer_id": 5,
         "name": "Bob Smith",
         "order_count": 22,
         "total_spent": 398.25,
         "avg_order_value": 18.10
       }
     ]
   }

Payment Breakdown
~~~~~~~~~~~~~~~~~

**GET /api/v1/dashboard/payment-breakdown**

Get payment method usage breakdown (cash/card/mobile).

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/payment-breakdown?start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD

**Response (200):**

.. code-block:: json

   [
     {
       "method": "card",
       "count": 185,
       "total_amount": 8542.50,
       "percentage": 56.1
     },
     {
       "method": "cash",
       "count": 112,
       "total_amount": 5124.30,
       "percentage": 32.8
     },
     {
       "method": "mobile",
       "count": 45,
       "total_amount": 1567.70,
       "percentage": 13.1
     }
   ]

Inventory Alerts
~~~~~~~~~~~~~~~~

**GET /api/v1/dashboard/inventory-alerts**

Get items with low or zero stock (excludes unlimited stock items).

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/inventory-alerts?threshold=10"

**Query Parameters:**

- ``threshold`` (int, optional): Low stock threshold, >= 0, default from settings

**Response (200):**

.. code-block:: json

   [
     {
       "item_id": 12,
       "name": "Croissant",
       "category": "Pastries",
       "stock_qty": 3,
       "status": "low_stock"
     },
     {
       "item_id": 18,
       "name": "Muffin",
       "category": "Pastries",
       "stock_qty": 0,
       "status": "out_of_stock"
     }
   ]

Profit & Loss
~~~~~~~~~~~~~

**GET /api/v1/dashboard/profit-loss**

Get profit and loss overview with expense breakdown.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/profit-loss?start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD

**Response (200):**

.. code-block:: json

   {
     "total_revenue": 15234.50,
     "total_expenses": 3420.75,
     "gross_profit": 11813.75,
     "profit_margin": 77.5,
     "total_tax_collected": 1218.76,
     "total_discounts_given": 542.30,
     "net_revenue": 13473.44,
     "expense_breakdown": [
       {
         "category": "supplies",
         "amount": 1850.00,
         "percentage": 54.1
       },
       {
         "category": "maintenance",
         "amount": 920.50,
         "percentage": 26.9
       },
       {
         "category": "utilities",
         "amount": 650.25,
         "percentage": 19.0
       }
     ]
   }

Shift Summary
~~~~~~~~~~~~~

**GET /api/v1/dashboard/shift-summary**

Get shift performance summaries with cash reconciliation.

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/shift-summary?shift_id=1"

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/v1/dashboard/shift-summary?start_date=2026-01-01&end_date=2026-01-31"

**Query Parameters:**

- ``shift_id`` (int, optional): Specific shift ID
- ``start_date`` (date, optional): Start date, format: YYYY-MM-DD
- ``end_date`` (date, optional): End date, format: YYYY-MM-DD

**Response (200):**

.. code-block:: json

   [
     {
       "shift_id": 1,
       "opened_at": "2026-01-15T08:00:00Z",
       "closed_at": "2026-01-15T16:00:00Z",
       "status": "closed",
       "total_orders": 42,
       "total_revenue": 765.50,
       "total_expenses": 120.00,
       "net": 645.50,
       "opening_cash": 200.0,
       "closing_cash": 485.50,
       "cash_difference": 0.0
     },
     {
       "shift_id": 2,
       "opened_at": "2026-01-15T16:00:00Z",
       "closed_at": "2026-01-16T00:00:00Z",
       "status": "closed",
       "total_orders": 38,
       "total_revenue": 698.30,
       "total_expenses": 85.50,
       "net": 612.80,
       "opening_cash": 200.0,
       "closing_cash": 512.80,
       "cash_difference": 0.0
     }
   ]
