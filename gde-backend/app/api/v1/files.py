"""
Files API endpoints for file uploads and imports.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import Profile
from ...services.file_service import FileService
from ..dependencies import get_current_user, require_contable

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    folder: str = Query("general", description="Target folder for the file")
):
    """
    Upload a file to the server.
    
    Args:
        file: File to upload
        db: Database session
        current_user: Current authenticated user
        folder: Target folder for the file
        
    Returns:
        dict: File upload details
    """
    service = FileService(db)
    
    try:
        result = await service.upload_file(
            file=file,
            folder=folder,
            user_id=str(current_user.id)
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )


@router.post("/upload/multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    folder: str = Query("general", description="Target folder for the files")
):
    """
    Upload multiple files to the server.
    
    Args:
        files: Files to upload
        db: Database session
        current_user: Current authenticated user
        folder: Target folder for the files
        
    Returns:
        dict: Upload results
    """
    service = FileService(db)
    
    results = []
    errors = []
    
    for file in files:
        try:
            result = await service.upload_file(
                file=file,
                folder=folder,
                user_id=str(current_user.id)
            )
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "uploaded": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


@router.delete("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Delete a file from the server.
    
    Args:
        file_id: File ID to delete
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If file not found or deletion fails
    """
    service = FileService(db)
    
    try:
        success = await service.delete_file(file_id, str(current_user.id))
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found or already deleted"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )


@router.post("/import/products", status_code=status.HTTP_201_CREATED)
async def import_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Import products from CSV/Excel file.
    
    Args:
        file: CSV or Excel file containing products data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Import results
    """
    service = FileService(db)
    
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV and Excel files are supported."
        )
    
    try:
        result = await service.import_products(
            file=file,
            user_id=str(current_user.id)
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing products: {str(e)}"
        )


@router.post("/import/costs", status_code=status.HTTP_201_CREATED)
async def import_costs(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Import costs from CSV/Excel file.
    
    Args:
        file: CSV or Excel file containing costs data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Import results
    """
    service = FileService(db)
    
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV and Excel files are supported."
        )
    
    try:
        result = await service.import_costs(
            file=file,
            user_id=str(current_user.id)
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing costs: {str(e)}"
        )


@router.post("/import/guides", status_code=status.HTTP_201_CREATED)
async def import_guides(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Import guides from CSV/Excel file.
    
    Args:
        file: CSV or Excel file containing guides data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Import results
    """
    service = FileService(db)
    
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV and Excel files are supported."
        )
    
    try:
        result = await service.import_guides(
            file=file,
            user_id=str(current_user.id)
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing guides: {str(e)}"
        )


@router.get("/import/history")
async def get_import_history(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """
    Get import history.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        
    Returns:
        List: Import history records
    """
    service = FileService(db)
    
    try:
        history = service.get_import_history(
            user_id=str(current_user.id),
            skip=skip,
            limit=limit
        )
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching import history: {str(e)}"
        )


@router.get("/import/{import_id}")
async def get_import_details(
    import_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get import details by ID.
    
    Args:
        import_id: Import log ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Import details
        
    Raises:
        HTTPException: If import not found
    """
    service = FileService(db)
    
    try:
        details = service.get_import_details(import_id)
        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Import record not found"
            )
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching import details: {str(e)}"
        )


@router.post("/export/template/{template_type}")
async def download_import_template(
    template_type: str,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Download import template file.
    
    Args:
        template_type: Type of template (products, costs, guides)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        File: Template file
        
    Raises:
        HTTPException: If template type is invalid
    """
    valid_templates = ["products", "costs", "guides"]
    
    if template_type not in valid_templates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid template type. Must be one of: {', '.join(valid_templates)}"
        )
    
    service = FileService(db)
    
    try:
        template = service.get_import_template(template_type)
        return template
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating template: {str(e)}"
        )






