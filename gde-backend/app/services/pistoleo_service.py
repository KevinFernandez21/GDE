"""
Pistoleo (scanning) service for barcode scanning sessions.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import secrets
import string

from ..models.pistoleo import PistoleoSession, Escaneo
from ..models.guia import Guia
from ..schemas.pistoleo import (
    PistoleoSessionCreate, PistoleoSessionUpdate,
    EscaneoCreate
)
from ..core.exceptions import NotFoundError, BusinessLogicError


class PistoleoService:
    """Service for managing scanning sessions."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _generate_qr_code(self, length: int = 12) -> str:
        """
        Generate a unique QR code for a session.
        
        Args:
            length: Length of the QR code
            
        Returns:
            str: Generated QR code
        """
        while True:
            code = ''.join(
                secrets.choice(string.ascii_uppercase + string.digits)
                for _ in range(length)
            )
            # Check if code already exists
            existing = self.db.query(PistoleoSession).filter(
                PistoleoSession.codigo_qr == code
            ).first()
            if not existing:
                return code
    
    def create_session(self, session_data: PistoleoSessionCreate, user_id: str) -> PistoleoSession:
        """
        Create a new pistoleo session.
        
        Args:
            session_data: Session creation data
            user_id: User creating the session
            
        Returns:
            PistoleoSession: Created session
        """
        # Generate unique QR code
        codigo_qr = self._generate_qr_code()
        
        session = PistoleoSession(
            codigo_qr=codigo_qr,
            usuario_id=user_id,
            nombre_sesion=session_data.nombre_sesion,
            ubicacion=session_data.ubicacion
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def get_sessions(
        self,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[PistoleoSession]:
        """
        Get pistoleo sessions.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            estado: Filter by estado
            user_id: Filter by user ID
            
        Returns:
            List[PistoleoSession]: List of sessions
        """
        query = self.db.query(PistoleoSession)
        
        if estado:
            query = query.filter(PistoleoSession.estado == estado)
        
        if user_id:
            query = query.filter(PistoleoSession.usuario_id == user_id)
        
        return query.order_by(desc(PistoleoSession.created_at)).offset(skip).limit(limit).all()
    
    def get_session(self, session_id: int) -> Optional[PistoleoSession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[PistoleoSession]: Session if found
        """
        return self.db.query(PistoleoSession).filter(PistoleoSession.id == session_id).first()
    
    def get_session_by_qr(self, codigo_qr: str) -> Optional[PistoleoSession]:
        """
        Get session by QR code.
        
        Args:
            codigo_qr: QR code
            
        Returns:
            Optional[PistoleoSession]: Session if found
        """
        return self.db.query(PistoleoSession).filter(
            PistoleoSession.codigo_qr == codigo_qr
        ).first()
    
    def update_session(
        self,
        session_id: int,
        session_data: PistoleoSessionUpdate
    ) -> Optional[PistoleoSession]:
        """
        Update pistoleo session.
        
        Args:
            session_id: Session ID
            session_data: Session update data
            
        Returns:
            Optional[PistoleoSession]: Updated session if found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)
        
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def complete_session(self, session_id: int) -> Optional[PistoleoSession]:
        """
        Mark session as completed.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[PistoleoSession]: Updated session if found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        session.estado = "completed"
        session.fecha_fin = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def cancel_session(self, session_id: int) -> Optional[PistoleoSession]:
        """
        Cancel session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[PistoleoSession]: Updated session if found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        session.estado = "cancelled"
        session.fecha_fin = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    # Escaneo (Scan) operations
    def create_scan(
        self,
        scan_data: EscaneoCreate,
        session_id: int,
        user_id: str
    ) -> Escaneo:
        """
        Create a new scan record.
        
        Args:
            scan_data: Scan data
            session_id: Session ID
            user_id: User performing the scan
            
        Returns:
            Escaneo: Created scan
            
        Raises:
            NotFoundError: If session not found
            BusinessLogicError: If session is not active
        """
        session = self.get_session(session_id)
        if not session:
            raise NotFoundError("PistoleoSession", session_id)
        
        if session.estado != "active":
            raise BusinessLogicError(f"Cannot scan in {session.estado} session")
        
        # Try to find guia by barcode
        guia = self.db.query(Guia).filter(Guia.codigo == scan_data.codigo_barras).first()
        
        # Check for duplicates
        estado_escaneo = "success"
        mensaje_error = None
        
        if guia:
            # Check if already scanned in this session
            existing_scan = self.db.query(Escaneo).filter(
                Escaneo.session_id == session_id,
                Escaneo.codigo_barras == scan_data.codigo_barras
            ).first()
            
            if existing_scan:
                estado_escaneo = "duplicate"
                mensaje_error = "Este código ya fue escaneado en esta sesión"
        else:
            estado_escaneo = "error"
            mensaje_error = "Guía no encontrada en el sistema"
        
        # Create scan record
        scan = Escaneo(
            session_id=session_id,
            guia_id=guia.id if guia else None,
            codigo_barras=scan_data.codigo_barras,
            tipo_codigo=scan_data.tipo_codigo,
            dispositivo=scan_data.dispositivo,
            usuario_id=user_id,
            ubicacion=scan_data.ubicacion,
            latitud=scan_data.latitud,
            longitud=scan_data.longitud,
            precision_gps=scan_data.precision_gps,
            imagen_url=scan_data.imagen_url,
            estado_escaneo=estado_escaneo,
            mensaje_error=mensaje_error,
            extra_data=scan_data.extra_data
        )
        
        self.db.add(scan)
        
        # Update session statistics
        session.escaneos_totales += 1
        if guia and estado_escaneo == "success":
            session.guias_procesadas += 1
        
        self.db.commit()
        self.db.refresh(scan)
        
        return scan
    
    def get_session_scans(
        self,
        session_id: int,
        skip: int = 0,
        limit: int = 100,
        estado_escaneo: Optional[str] = None
    ) -> List[Escaneo]:
        """
        Get scans for a session.
        
        Args:
            session_id: Session ID
            skip: Number of records to skip
            limit: Number of records to return
            estado_escaneo: Filter by scan status
            
        Returns:
            List[Escaneo]: List of scans
        """
        query = self.db.query(Escaneo).filter(Escaneo.session_id == session_id)
        
        if estado_escaneo:
            query = query.filter(Escaneo.estado_escaneo == estado_escaneo)
        
        return query.order_by(desc(Escaneo.fecha_escaneo)).offset(skip).limit(limit).all()
    
    def get_session_statistics(self, session_id: int) -> dict:
        """
        Get session statistics.
        
        Args:
            session_id: Session ID
            
        Returns:
            dict: Session statistics
        """
        session = self.get_session(session_id)
        if not session:
            return {}
        
        scans = self.get_session_scans(session_id, limit=10000)
        
        success_scans = [s for s in scans if s.estado_escaneo == "success"]
        error_scans = [s for s in scans if s.estado_escaneo == "error"]
        duplicate_scans = [s for s in scans if s.estado_escaneo == "duplicate"]
        
        duration = None
        if session.fecha_fin:
            duration = (session.fecha_fin - session.fecha_inicio).total_seconds()
        elif session.estado == "active":
            duration = (datetime.utcnow() - session.fecha_inicio).total_seconds()
        
        return {
            "session_id": session.id,
            "codigo_qr": session.codigo_qr,
            "nombre_sesion": session.nombre_sesion,
            "estado": session.estado,
            "escaneos_totales": len(scans),
            "escaneos_exitosos": len(success_scans),
            "escaneos_error": len(error_scans),
            "escaneos_duplicados": len(duplicate_scans),
            "guias_procesadas": session.guias_procesadas,
            "duracion_segundos": duration,
            "fecha_inicio": session.fecha_inicio,
            "fecha_fin": session.fecha_fin
        }






