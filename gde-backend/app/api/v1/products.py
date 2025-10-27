"""
Products API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    ProductResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    StockAlertResponse,
    InventoryReportResponse
)
from ...services.product_service import ProductService
from ..dependencies import get_current_user, require_contable, get_pagination_params

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new product.
    
    Args:
        product_data: Product creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ProductResponse: Created product
    """
    service = ProductService(db)
    product = service.create_product(product_data, str(current_user.id))
    return product


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name or code"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """
    Get products with optional filtering.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        search: Search term for name or code
        category_id: Filter by category ID
        status: Filter by status
        
    Returns:
        List[ProductResponse]: List of products
    """
    service = ProductService(db)
    products = service.get_products(
        skip=skip,
        limit=limit,
        search=search,
        category_id=category_id,
        status=status
    )
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get product by ID.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ProductResponse: Product details
        
    Raises:
        HTTPException: If product not found
    """
    service = ProductService(db)
    product = service.get_product(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update product.
    
    Args:
        product_id: Product ID
        product_data: Product update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ProductResponse: Updated product
        
    Raises:
        HTTPException: If product not found
    """
    service = ProductService(db)
    product = service.update_product(product_id, product_data, str(current_user.id))
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete product.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If product not found
    """
    service = ProductService(db)
    success = service.delete_product(product_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product deleted successfully"}


@router.get("/{product_id}/stock", response_model=ProductResponse)
async def get_product_stock(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get product stock information.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ProductResponse: Product with stock information
        
    Raises:
        HTTPException: If product not found
    """
    service = ProductService(db)
    product = service.get_product(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.get("/alerts/low-stock", response_model=List[StockAlertResponse])
async def get_low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    threshold: Optional[int] = Query(None, description="Stock threshold")
):
    """
    Get products with low stock alerts.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        threshold: Stock threshold (uses product's stock_minimo if not provided)
        
    Returns:
        List[StockAlertResponse]: Products with low stock
    """
    service = ProductService(db)
    products = service.get_low_stock_products(threshold)
    
    alerts = []
    for product in products:
        alert_type = "out_of_stock" if product.stock_actual == 0 else "low_stock"
        severity = "critical" if product.stock_actual == 0 else "warning"
        
        alerts.append(StockAlertResponse(
            product_id=product.id,
            product_name=product.name,
            current_stock=product.stock_actual,
            minimum_stock=product.stock_minimo,
            alert_type=alert_type,
            severity=severity
        ))
    
    return alerts


@router.get("/inventory/summary", response_model=InventoryReportResponse)
async def get_inventory_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get inventory summary statistics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        InventoryReportResponse: Inventory summary
    """
    service = ProductService(db)
    summary = service.get_inventory_summary()
    
    return InventoryReportResponse(
        total_products=summary["total_products"],
        total_value=summary["total_value"],
        low_stock_products=summary["low_stock_products"],
        out_of_stock_products=summary["out_of_stock_products"],
        categories_summary=[]  # TODO: Implement categories summary
    )


# Category endpoints
@router.post("/categories/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new category.
    
    Args:
        category_data: Category creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CategoryResponse: Created category
    """
    service = ProductService(db)
    category = service.create_category(category_data)
    return category


@router.get("/categories/", response_model=List[CategoryResponse])
async def get_categories(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    active_only: bool = Query(True, description="Return only active categories")
):
    """
    Get categories.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        active_only: Whether to return only active categories
        
    Returns:
        List[CategoryResponse]: List of categories
    """
    service = ProductService(db)
    categories = service.get_categories(active_only=active_only)
    return categories


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get category by ID.
    
    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CategoryResponse: Category details
        
    Raises:
        HTTPException: If category not found
    """
    service = ProductService(db)
    category = service.get_category(category_id)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update category.
    
    Args:
        category_id: Category ID
        category_data: Category update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CategoryResponse: Updated category
        
    Raises:
        HTTPException: If category not found
    """
    service = ProductService(db)
    category = service.update_category(category_id, category_data)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete category.
    
    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If category not found or has products
    """
    service = ProductService(db)
    success = service.delete_category(category_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return {"message": "Category deleted successfully"}
