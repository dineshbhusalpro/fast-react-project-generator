#!/usr/bin/env python3
"""
Add new microservice to existing FastAPI project
Usage: python fastapi_service_generator.py add-service <service_name>
"""

import argparse
import sys
from pathlib import Path

def add_service_to_project(service_name: str, port: int = None):
    """Add a new microservice to existing project"""
    
    # Check if we're in a FastAPI project
    if not Path("backend/services").exists():
        print("❌ Not in a FastAPI project directory!")
        print("Run this from the project root where backend/services exists.")
        sys.exit(1)
    
    service_path = Path("backend/services") / service_name
    
    if service_path.exists():
        print(f"❌ Service '{service_name}' already exists!")
        sys.exit(1)
    
    print(f"📦 Adding microservice: {service_name}")
    
    # Create service structure
    directories = [
        "app/models",
        "app/schemas",
        "app/database", 
        "app/services",
        "app/routes",
        "tests"
    ]
    
    for directory in directories:
        (service_path / directory).mkdir(parents=True, exist_ok=True)
        (service_path / directory / "__init__.py").touch()
    
    # Determine port
    if not port:
        existing_services = [d for d in Path("backend/services").iterdir() if d.is_dir()]
        port = 8001 + len(existing_services)
    
    # Create service files
    create_service_files(service_path, service_name, port)
    
    print(f"✅ Service '{service_name}' created successfully!")
    print(f"🔗 Service will run on port {port}")
    print(f"📝 Don't forget to add it to docker-compose.yml")

def create_service_files(service_path: Path, service_name: str, port: int):
    """Create the main files for a new service"""
    
    # main.py
    main_content = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import {service_name.split('_')[0]}
from app.config import settings

app = FastAPI(
    title="{service_name.replace('_', ' ').title()} Service",
    description="Microservice for {service_name.replace('_', ' ')} functionality",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router({service_name.split('_')[0]}.router)

@app.get("/health")
def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True
    )
'''
    
    # config.py with dynamic port
    config_content = f'''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/url_shortener"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Service
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = {port}
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"

settings = Settings()
'''
    
    # Basic route file
    route_content = f'''from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/v1/{service_name.split('_')[0]}", tags=["{service_name.split('_')[0]}"])

@router.get("/")
def get_{service_name.split('_')[0]}_list():
    """Get list of {service_name.split('_')[0]} items"""
    return {{"message": "Hello from {service_name}!"}}

@router.post("/")
def create_{service_name.split('_')[0]}():
    """Create new {service_name.split('_')[0]} item"""
    return {{"message": "{service_name.split('_')[0].title()} created successfully"}}
'''
    
    # requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
redis==5.0.1
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
'''
    
    # Write files
    (service_path / "app/main.py").write_text(main_content)
    (service_path / "app/config.py").write_text(config_content)
    (service_path / f"app/routes/{service_name.split('_')[0]}.py").write_text(route_content)
    (service_path / "requirements.txt").write_text(requirements_content)

def main():
    parser = argparse.ArgumentParser(description="FastAPI Service Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add service command
    add_parser = subparsers.add_parser("add-service", help="Add new microservice")
    add_parser.add_argument("service_name", help="Name of the service to create")
    add_parser.add_argument("--port", type=int, help="Port number for the service")
    
    args = parser.parse_args()
    
    if args.command == "add-service":
        add_service_to_project(args.service_name, args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()