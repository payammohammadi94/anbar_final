# API Documentation - Warehouse Management System

## Overview
This API provides comprehensive access to all warehouse management models with full relationship support.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Available Endpoints

### 1. Categories (دسته‌بندی‌ها)
- **GET** `/api/categories/` - List all categories
- **POST** `/api/categories/` - Create new category
- **GET** `/api/categories/{id}/` - Get specific category
- **PUT** `/api/categories/{id}/` - Update category
- **DELETE** `/api/categories/{id}/` - Delete category
- **GET** `/api/categories/{id}/sub_categories/` - Get sub-categories
- **GET** `/api/categories/main_categories/` - Get main categories only

### 2. Responsible Persons (مسئولین)
- **GET** `/api/responsible-testing/` - List testing responsible persons
- **GET** `/api/responsible-qc/` - List QC responsible persons

### 3. Product Information (اطلاعات محصولات)
- **GET** `/api/product-parts/` - List product parts
- **GET** `/api/product-codes/` - List product codes

### 4. Quarantine Warehouse (انبار قرنطینه)
- **GET** `/api/quarantine-warehouse/` - List all quarantine items
- **POST** `/api/quarantine-warehouse/` - Add new quarantine item
- **GET** `/api/quarantine-warehouse/{id}/` - Get specific item
- **PUT** `/api/quarantine-warehouse/{id}/` - Update item
- **DELETE** `/api/quarantine-warehouse/{id}/` - Delete item
- **GET** `/api/quarantine-warehouse/by_status/?status=waiting_test` - Filter by status
- **GET** `/api/quarantine-warehouse/statistics/` - Get statistics

### 5. Raw Material Warehouse (انبار مواد اولیه)
- **GET** `/api/raw-material-warehouse/` - List all raw materials
- **POST** `/api/raw-material-warehouse/` - Add new raw material
- **GET** `/api/raw-material-warehouse/{id}/` - Get specific material
- **PUT** `/api/raw-material-warehouse/{id}/` - Update material
- **DELETE** `/api/raw-material-warehouse/{id}/` - Delete material
- **GET** `/api/raw-material-warehouse/low_stock/?threshold=10` - Get low stock items
- **GET** `/api/raw-material-warehouse/statistics/` - Get statistics

### 6. Product Warehouse (انبار محصولات)
- **GET** `/api/product-warehouse/` - List all products
- **POST** `/api/product-warehouse/` - Add new product
- **GET** `/api/product-warehouse/{id}/` - Get specific product
- **PUT** `/api/product-warehouse/{id}/` - Update product
- **DELETE** `/api/product-warehouse/{id}/` - Delete product
- **GET** `/api/product-warehouse/in_progress/` - Get products in progress
- **GET** `/api/product-warehouse/completed/` - Get completed products
- **GET** `/api/product-warehouse/{id}/raw_materials/` - Get product raw materials
- **GET** `/api/product-warehouse/{id}/secondry_products/` - Get product secondary products

### 7. Secondary Warehouse (انبار ثانویه)
- **GET** `/api/secondry-warehouse/` - List all secondary products
- **POST** `/api/secondry-warehouse/` - Add new secondary product
- **GET** `/api/secondry-warehouse/{id}/` - Get specific secondary product
- **PUT** `/api/secondry-warehouse/{id}/` - Update secondary product
- **DELETE** `/api/secondry-warehouse/{id}/` - Delete secondary product
- **GET** `/api/secondry-warehouse/in_progress/` - Get secondary products in progress
- **GET** `/api/secondry-warehouse/{id}/raw_materials/` - Get secondary product raw materials

### 8. Product Materials (مواد محصولات)
- **GET** `/api/product-raw-materials/` - List product raw materials
- **GET** `/api/secondry-warehouse-raw-materials/` - List secondary warehouse raw materials
- **GET** `/api/product-secondry-products/` - List product-secondary product relationships

### 9. Product Deliveries (تحویل محصولات)
- **GET** `/api/product-deliveries/` - List all product deliveries
- **POST** `/api/product-deliveries/` - Create new delivery
- **GET** `/api/product-deliveries/{id}/` - Get specific delivery
- **PUT** `/api/product-deliveries/{id}/` - Update delivery
- **DELETE** `/api/product-deliveries/{id}/` - Delete delivery
- **GET** `/api/product-deliveries/pending_return/` - Get pending returns
- **GET** `/api/product-deliveries/{id}/items/` - Get all delivery items

### 10. External Deliveries (تحویل‌های خارجی)
- **GET** `/api/external-product-deliveries/` - List external deliveries
- **POST** `/api/external-product-deliveries/` - Create external delivery
- **GET** `/api/external-product-deliveries/{id}/` - Get specific external delivery
- **PUT** `/api/external-product-deliveries/{id}/` - Update external delivery
- **DELETE** `/api/external-product-deliveries/{id}/` - Delete external delivery
- **GET** `/api/external-product-deliveries/pending_return/` - Get pending external returns
- **GET** `/api/external-product-deliveries/{id}/items/` - Get all external delivery items

### 11. Returned Products (محصولات برگشتی)
- **GET** `/api/returned-products/` - List returned products to supplier
- **GET** `/api/returned-from-customer/` - List products returned by customers

### 12. Borrowed Products (امانی‌ها)
- **GET** `/api/borrowed-products/` - List borrowed products
- **GET** `/api/borrowed-products/pending_return/` - Get pending borrowed returns

## Filtering and Search

All endpoints support:
- **Search**: Use `?search=term` to search across relevant fields
- **Filtering**: Use field-specific filters like `?status=waiting_test`
- **Ordering**: Use `?ordering=field_name` or `?ordering=-field_name` for descending
- **Pagination**: Automatic pagination with `?page=1&page_size=20`

## Example Requests

### Create a new quarantine item:
```json
POST /api/quarantine-warehouse/
{
    "piece_name": "قطعه نمونه",
    "item_code_id": 1,
    "quantity": 10,
    "entry_date": "2024-01-15",
    "unit_price": 100.50,
    "unit": "dollar",
    "supplier": "تامین کننده نمونه",
    "status": "waiting_test",
    "category_ids": [1, 2]
}
```

### Get products in progress:
```
GET /api/product-warehouse/in_progress/
```

### Get low stock raw materials:
```
GET /api/raw-material-warehouse/low_stock/?threshold=5
```

### Search for items:
```
GET /api/quarantine-warehouse/?search=قطعه&status=approved
```

## Response Format

All responses follow this format:
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses include detailed error messages:
```json
{
    "error": "Error message in Persian"
}
```

## Notes

1. All dates should be in YYYY-MM-DD format
2. Decimal fields support up to 10 digits with 2 decimal places
3. All foreign key relationships are properly serialized with full object details
4. Many-to-many relationships are handled automatically
5. The API supports both Persian and English field names


