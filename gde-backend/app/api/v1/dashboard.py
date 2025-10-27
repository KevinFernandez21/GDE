"""
Dashboard API endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ...core.database import get_db
from ...models.user import Profile
from ...models.product import Product
from ...models.guia import Guia, GuiaItem
from ...models.costo import Costo
from ...models.pistoleo import PistoleoSession
from ..dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics")
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get dashboard metrics and statistics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict containing all dashboard metrics
    """
    
    # Inventario y Stock
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_stock = db.query(func.sum(Product.stock_actual)).scalar() or 0
    
    # Stock OK (por encima del mínimo)
    stock_ok = db.query(func.count(Product.id)).filter(
        Product.stock_actual > Product.stock_minimo
    ).scalar() or 0
    
    # Stock Bajo (por debajo del mínimo pero mayor a 0)
    stock_bajo = db.query(func.count(Product.id)).filter(
        Product.stock_actual <= Product.stock_minimo,
        Product.stock_actual > 0
    ).scalar() or 0
    
    # Agotados (stock = 0)
    agotados = db.query(func.count(Product.id)).filter(
        Product.stock_actual == 0
    ).scalar() or 0
    
    # Métricas Financieras
    # Valor inventario (costo de compra)
    valor_inventario = db.query(
        func.sum(Product.precio_costo * Product.stock_actual)
    ).scalar() or 0
    
    # Valor venta potencial
    valor_venta_potencial = db.query(
        func.sum(Product.precio_venta * Product.stock_actual)
    ).scalar() or 0
    
    # Margen potencial
    margen_potencial = valor_venta_potencial - valor_inventario
    
    # Costos totales
    costos_totales = db.query(func.sum(Costo.monto)).filter(
        Costo.activo == True
    ).scalar() or 0
    
    # Capital total (suma de aportes y préstamos)
    capital_aportes = db.query(func.sum(Costo.monto)).filter(
        Costo.tipo == "aporte",
        Costo.activo == True
    ).scalar() or 0
    
    capital_prestamos = db.query(func.sum(Costo.monto)).filter(
        Costo.tipo == "prestamo",
        Costo.activo == True
    ).scalar() or 0
    
    capital_total = capital_aportes + capital_prestamos
    
    # Seguimiento de Guías
    # Total guías master
    total_guias_master = db.query(func.count(Guia.id)).filter(
        Guia.tipo == "master"
    ).scalar() or 0
    
    # Guías último mes
    ultimo_mes = datetime.utcnow() - timedelta(days=30)
    guias_ultimo_mes = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= ultimo_mes
    ).scalar() or 0
    
    # Guías escaneadas
    guias_escaneadas = db.query(func.count(Guia.id)).filter(
        Guia.estado == "escaneado"
    ).scalar() or 0
    
    # Guías pendientes
    guias_pendientes = db.query(func.count(Guia.id)).filter(
        Guia.estado == "pendiente"
    ).scalar() or 0
    
    # Guías desconocidas (duplicadas)
    guias_desconocidas = db.query(func.count(Guia.id)).filter(
        Guia.estado == "duplicado"
    ).scalar() or 0
    
    # Guías duplicadas (multi-scan)
    guias_duplicadas = db.query(func.count(Guia.id)).filter(
        Guia.estado == "multi_scan"
    ).scalar() or 0
    
    # Porcentaje completado
    porcentaje_completado = 0
    if total_guias_master > 0:
        porcentaje_completado = (guias_escaneadas / total_guias_master) * 100
    
    # Actividad de Escaneo (Hoy)
    hoy_inicio = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = hoy_inicio + timedelta(days=1)
    
    # Sesiones activas hoy
    sesiones_activas = db.query(func.count(PistoleoSession.id)).filter(
        PistoleoSession.created_at >= hoy_inicio,
        PistoleoSession.created_at < hoy_fin,
        PistoleoSession.estado == "activa"
    ).scalar() or 0
    
    # Total escaneos hoy
    total_escaneos_hoy = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= hoy_inicio,
        Guia.created_at < hoy_fin
    ).scalar() or 0
    
    # Guías escaneadas hoy (únicas)
    guias_escaneadas_hoy = db.query(func.count(func.distinct(Guia.codigo))).filter(
        Guia.created_at >= hoy_inicio,
        Guia.created_at < hoy_fin
    ).scalar() or 0
    
    # Productos escaneados hoy (total items)
    productos_escaneados_hoy = db.query(func.sum(GuiaItem.cantidad)).join(
        Guia, GuiaItem.guia_id == Guia.id
    ).filter(
        Guia.created_at >= hoy_inicio,
        Guia.created_at < hoy_fin
    ).scalar() or 0
    
    # Guías de Despacho (Último mes)
    total_guias_despacho = guias_ultimo_mes
    
    # Estados de guías último mes
    pendientes_mes = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= ultimo_mes,
        Guia.estado == "pendiente"
    ).scalar() or 0
    
    en_transito_mes = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= ultimo_mes,
        Guia.estado == "en_transito"
    ).scalar() or 0
    
    entregadas_mes = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= ultimo_mes,
        Guia.estado == "entregado"
    ).scalar() or 0
    
    # Porcentaje entregadas
    porcentaje_entregadas = 0
    if total_guias_despacho > 0:
        porcentaje_entregadas = (entregadas_mes / total_guias_despacho) * 100
    
    # Construir respuesta
    return {
        "inventario_stock": {
            "total_productos": total_products,
            "total_stock": int(total_stock),
            "stock_ok": stock_ok,
            "stock_bajo": stock_bajo,
            "agotados": agotados,
            "porcentaje_stock_saludable": round((stock_ok / total_products * 100) if total_products > 0 else 0, 2)
        },
        "metricas_financieras": {
            "valor_inventario": float(valor_inventario),
            "valor_venta_potencial": float(valor_venta_potencial),
            "margen_potencial": float(margen_potencial),
            "costos_totales": float(costos_totales),
            "capital_total": float(capital_total),
            "capital_aportes": float(capital_aportes),
            "capital_prestamos": float(capital_prestamos)
        },
        "seguimiento_guias": {
            "total_guias_master": total_guias_master,
            "escaneadas": guias_escaneadas,
            "pendientes": guias_pendientes,
            "desconocidas": guias_desconocidas,
            "duplicadas": guias_duplicadas,
            "porcentaje_completado": round(porcentaje_completado, 2)
        },
        "actividad_escaneo_hoy": {
            "sesiones_activas": sesiones_activas,
            "total_escaneos": total_escaneos_hoy,
            "guias_escaneadas": guias_escaneadas_hoy,
            "productos_escaneados": int(productos_escaneados_hoy)
        },
        "guias_despacho_mes": {
            "total": total_guias_despacho,
            "pendientes": pendientes_mes,
            "en_transito": en_transito_mes,
            "entregadas": entregadas_mes,
            "porcentaje_entregadas": round(porcentaje_entregadas, 2)
        },
        "timestamp": datetime.utcnow().isoformat(),
        "periodo": {
            "mes_inicio": ultimo_mes.isoformat(),
            "hoy_inicio": hoy_inicio.isoformat()
        }
    }


@router.get("/activity-summary")
async def get_activity_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get system activity summary.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict containing activity summary
    """
    
    # Últimas 24 horas
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    # Nuevos productos
    nuevos_productos = db.query(func.count(Product.id)).filter(
        Product.created_at >= last_24h
    ).scalar() or 0
    
    # Nuevas guías
    nuevas_guias = db.query(func.count(Guia.id)).filter(
        Guia.created_at >= last_24h
    ).scalar() or 0
    
    # Actualizaciones de stock
    actualizaciones_stock = db.query(func.count(Product.id)).filter(
        Product.updated_at >= last_24h
    ).scalar() or 0
    
    return {
        "periodo": "24h",
        "nuevos_productos": nuevos_productos,
        "nuevas_guias": nuevas_guias,
        "actualizaciones_stock": actualizaciones_stock,
        "timestamp": datetime.utcnow().isoformat()
    }

