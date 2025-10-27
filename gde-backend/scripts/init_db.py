#!/usr/bin/env python3
"""
Database initialization script for GDE Backend API.
"""
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))

from app.core.database import create_tables, SessionLocal
from app.core.config import settings
from app.models import *  # Import all models
from app.core.security import get_password_hash


def main():
    """Initialize the database."""
    print("🗄️  Initializing GDE Backend Database...")
    print(f"📊 Database URL: {settings.database_url}")
    print("-" * 50)
    
    try:
        # Create all tables
        create_tables()
        print("✅ Database tables created successfully!")
        
        print("🌱 Seeding initial data (roles, users)...")
        seed_initial_data()
        print("✅ Initial data seeded successfully!")
        
        print("🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


def seed_initial_data():
    """Seed initial roles and demo users."""
    db = SessionLocal()
    try:
        # Ensure roles
        role_admin = db.query(Role).filter(Role.name == "admin").first()
        if not role_admin:
            role_admin = Role(name="admin", description="Administrador", permissions={"*": ["*"]})
            db.add(role_admin)

        role_contable = db.query(Role).filter(Role.name == "contable").first()
        if not role_contable:
            role_contable = Role(name="contable", description="Contable", permissions={"inventario": ["r"], "guias": ["r"]})
            db.add(role_contable)

        db.commit()

        def upsert_user(username: str, email: str, full_name: str, password: str, role: str):
            user = db.query(Profile).filter(Profile.username == username).first()
            if not user:
                user = Profile(
                    username=username,
                    full_name=full_name,
                    email=email,
                    role=role,
                    password_hash=get_password_hash(password),
                    is_active=True,
                )
                db.add(user)
                db.commit()
                print(f"   - Created user: {username} ({role})")
            else:
                # ensure fields are up to date
                user.full_name = full_name
                user.email = email
                user.role = role
                user.password_hash = get_password_hash(password)
                db.commit()
                print(f"   - Updated user: {username} ({role})")

        upsert_user(
            username="taylor",
            email="taylor.contador@gde.com",
            full_name="Taylor",
            password="taylor2024",
            role="contable",
        )
        upsert_user(
            username="alejandro",
            email="alejandro.contador@gde.com",
            full_name="Alejandro",
            password="alejandro2024",
            role="contable",
        )
        upsert_user(
            username="daniel",
            email="daniel.admin@gde.com",
            full_name="Daniel",
            password="daniel2024",
            role="admin",
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
