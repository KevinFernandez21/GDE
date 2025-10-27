"""
File processing service for Excel/CSV imports.
"""
import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from sqlalchemy.orm import Session

from ..models.audit import ImportLog
from ..core.exceptions import FileProcessingError

logger = logging.getLogger(__name__)


class FileService:
    """Service for file processing operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_excel_file(
        self, 
        file_path: str, 
        entity_type: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process Excel file for data import.
        
        Args:
            file_path: Path to the Excel file
            entity_type: Type of entity to import (products, guias, costos, etc.)
            user_id: ID of the user performing the import
            
        Returns:
            Dict[str, Any]: Processing results
            
        Raises:
            FileProcessingError: If file processing fails
        """
        try:
            # Create import log
            import_log = ImportLog(
                usuario_id=user_id,
                archivo=Path(file_path).name,
                tipo_archivo="excel",
                entidad=entity_type,
                estado="processing"
            )
            self.db.add(import_log)
            self.db.commit()
            self.db.refresh(import_log)
            
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate data
            validated_data = self._validate_data(df, entity_type)
            
            # Process data
            processed_data = self._process_data(validated_data, entity_type)
            
            # Update import log
            import_log.registros_totales = len(df)
            import_log.registros_exitosos = len(processed_data['success'])
            import_log.registros_fallidos = len(processed_data['errors'])
            import_log.errores = processed_data['errors']
            import_log.estado = "completed"
            import_log.fecha_procesamiento = pd.Timestamp.now()
            
            self.db.commit()
            
            return {
                "import_log_id": import_log.id,
                "total_records": len(df),
                "successful_records": len(processed_data['success']),
                "failed_records": len(processed_data['errors']),
                "errors": processed_data['errors'],
                "success_data": processed_data['success']
            }
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {e}")
            
            # Update import log with error
            if 'import_log' in locals():
                import_log.estado = "failed"
                import_log.errores = {"error": str(e)}
                self.db.commit()
            
            raise FileProcessingError(f"Error processing Excel file: {str(e)}")
    
    def process_csv_file(
        self, 
        file_path: str, 
        entity_type: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process CSV file for data import.
        
        Args:
            file_path: Path to the CSV file
            entity_type: Type of entity to import
            user_id: ID of the user performing the import
            
        Returns:
            Dict[str, Any]: Processing results
            
        Raises:
            FileProcessingError: If file processing fails
        """
        try:
            # Create import log
            import_log = ImportLog(
                usuario_id=user_id,
                archivo=Path(file_path).name,
                tipo_archivo="csv",
                entidad=entity_type,
                estado="processing"
            )
            self.db.add(import_log)
            self.db.commit()
            self.db.refresh(import_log)
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Validate data
            validated_data = self._validate_data(df, entity_type)
            
            # Process data
            processed_data = self._process_data(validated_data, entity_type)
            
            # Update import log
            import_log.registros_totales = len(df)
            import_log.registros_exitosos = len(processed_data['success'])
            import_log.registros_fallidos = len(processed_data['errors'])
            import_log.errores = processed_data['errors']
            import_log.estado = "completed"
            import_log.fecha_procesamiento = pd.Timestamp.now()
            
            self.db.commit()
            
            return {
                "import_log_id": import_log.id,
                "total_records": len(df),
                "successful_records": len(processed_data['success']),
                "failed_records": len(processed_data['errors']),
                "errors": processed_data['errors'],
                "success_data": processed_data['success']
            }
            
        except Exception as e:
            logger.error(f"Error processing CSV file: {e}")
            
            # Update import log with error
            if 'import_log' in locals():
                import_log.estado = "failed"
                import_log.errores = {"error": str(e)}
                self.db.commit()
            
            raise FileProcessingError(f"Error processing CSV file: {str(e)}")
    
    def _validate_data(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        """
        Validate data based on entity type.
        
        Args:
            df: DataFrame to validate
            entity_type: Type of entity
            
        Returns:
            pd.DataFrame: Validated DataFrame
            
        Raises:
            FileProcessingError: If validation fails
        """
        if entity_type == "products":
            required_columns = ["code", "name", "stock_actual"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise FileProcessingError(f"Missing required columns: {missing_columns}")
        
        elif entity_type == "guias":
            required_columns = ["codigo", "cliente_nombre"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise FileProcessingError(f"Missing required columns: {missing_columns}")
        
        elif entity_type == "costos":
            required_columns = ["fecha", "descripcion", "monto"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise FileProcessingError(f"Missing required columns: {missing_columns}")
        
        else:
            raise FileProcessingError(f"Unsupported entity type: {entity_type}")
        
        return df
    
    def _process_data(self, df: pd.DataFrame, entity_type: str) -> Dict[str, List]:
        """
        Process validated data.
        
        Args:
            df: Validated DataFrame
            entity_type: Type of entity
            
        Returns:
            Dict[str, List]: Processed data with success and error lists
        """
        success = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                if entity_type == "products":
                    processed_row = self._process_product_row(row)
                    success.append(processed_row)
                elif entity_type == "guias":
                    processed_row = self._process_guia_row(row)
                    success.append(processed_row)
                elif entity_type == "costos":
                    processed_row = self._process_costo_row(row)
                    success.append(processed_row)
                else:
                    raise ValueError(f"Unsupported entity type: {entity_type}")
                    
            except Exception as e:
                errors.append({
                    "row": index + 1,
                    "error": str(e),
                    "data": row.to_dict()
                })
        
        return {
            "success": success,
            "errors": errors
        }
    
    def _process_product_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process a single product row."""
        return {
            "code": str(row.get("code", "")),
            "name": str(row.get("name", "")),
            "description": str(row.get("description", "")),
            "stock_actual": int(row.get("stock_actual", 0)),
            "stock_minimo": int(row.get("stock_minimo", 10)),
            "precio_compra": float(row.get("precio_compra", 0)),
            "precio_venta": float(row.get("precio_venta", 0)),
            "categoria_id": int(row.get("categoria_id", 0)) if pd.notna(row.get("categoria_id")) else None,
            "proveedor": str(row.get("proveedor", "")),
            "marca": str(row.get("marca", "")),
            "modelo": str(row.get("modelo", "")),
            "ubicacion_bodega": str(row.get("ubicacion_bodega", "")),
            "codigo_barras": str(row.get("codigo_barras", "")),
            "status": str(row.get("status", "active"))
        }
    
    def _process_guia_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process a single guia row."""
        return {
            "codigo": str(row.get("codigo", "")),
            "cliente_nombre": str(row.get("cliente_nombre", "")),
            "cliente_ruc": str(row.get("cliente_ruc", "")),
            "cliente_direccion": str(row.get("cliente_direccion", "")),
            "cliente_telefono": str(row.get("cliente_telefono", "")),
            "cliente_email": str(row.get("cliente_email", "")),
            "direccion_entrega": str(row.get("direccion_entrega", "")),
            "transportista": str(row.get("transportista", "")),
            "observaciones": str(row.get("observaciones", ""))
        }
    
    def _process_costo_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process a single costo row."""
        return {
            "fecha": str(row.get("fecha", "")),
            "descripcion": str(row.get("descripcion", "")),
            "monto": float(row.get("monto", 0)),
            "categoria_id": int(row.get("categoria_id", 0)) if pd.notna(row.get("categoria_id")) else None,
            "proveedor": str(row.get("proveedor", "")),
            "documento": str(row.get("documento", "")),
            "numero_documento": str(row.get("numero_documento", "")),
            "tipo_documento": str(row.get("tipo_documento", "")),
            "estado": str(row.get("estado", "pendiente")),
            "metodo_pago": str(row.get("metodo_pago", "transferencia")),
            "observaciones": str(row.get("observaciones", ""))
        }
    
    def get_import_logs(
        self, 
        user_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        limit: int = 100
    ) -> List[ImportLog]:
        """
        Get import logs.
        
        Args:
            user_id: Filter by user ID
            entity_type: Filter by entity type
            limit: Maximum number of records to return
            
        Returns:
            List[ImportLog]: List of import logs
        """
        query = self.db.query(ImportLog)
        
        if user_id:
            query = query.filter(ImportLog.usuario_id == user_id)
        
        if entity_type:
            query = query.filter(ImportLog.entidad == entity_type)
        
        return query.order_by(ImportLog.created_at.desc()).limit(limit).all()
    
    def get_import_log(self, log_id: int) -> Optional[ImportLog]:
        """
        Get import log by ID.
        
        Args:
            log_id: Import log ID
            
        Returns:
            Optional[ImportLog]: Import log if found
        """
        return self.db.query(ImportLog).filter(ImportLog.id == log_id).first()
