#!/usr/bin/env python3
"""
FastAPI Project Generator CLI Tool
Similar to Django's startproject but for FastAPI microservices
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List
import json

class FastAPIProjectGenerator:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.base_path = Path(project_name)
        
    def create_project_structure(self):
        """Create the main project directory structure"""
        print(f"🚀 Creating FastAPI project: {self.project_name}")
        
        # Main directories
        directories = [
            "backend/api_gateway/app/routes",
            "backend/api_gateway/tests",
            "backend/services",
            "backend/shared",
            "frontend/src/components/common",
            "frontend/src/components/forms", 
            "frontend/src/components/auth",
            "frontend/src/pages",
            "frontend/src/services",
            "frontend/src/config",
            "frontend/public",
            "frontend/tests",
            "docs",
            "scripts",
            ".github/workflows"
        ]
        
        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)
            
        print("✅ Project structure created")
        
    def create_microservice(self, service_name: str):
        """Create a microservice with FastAPI structure"""
        print(f"📦 Creating microservice: {service_name}")
        
        service_path = self.base_path / "backend/services" / service_name
        
        # Service directories
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
            
        # Create __init__.py files
        for directory in directories:
            (service_path / directory / "__init__.py").touch()
            
        # Create main files
        self._create_service_files(service_path, service_name)
        print(f"✅ Microservice {service_name} created")
        
    def _create_service_files(self, service_path: Path, service_name: str):
        """Create the main files for a microservice"""
        
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
        
        # config.py
        config_content = '''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/url_shortener"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Service
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8001
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
'''
        
        # requirements.txt
        requirements_content = '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
redis==5.0.1
passlib==1.7.4
python-jose[cryptography]==3.3.0
bcrypt==4.1.2
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==0.47.0
'''
        
        # Dockerfile
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
'''
        
        # Write files
        (service_path / "app/main.py").write_text(main_content)
        (service_path / "app/config.py").write_text(config_content)
        (service_path / "requirements.txt").write_text(requirements_content)
        (service_path / "Dockerfile").write_text(dockerfile_content)
        
    def create_react_frontend(self):
        """Initialize React frontend"""
        print("⚛️  Creating React frontend...")
        
        frontend_path = self.base_path / "frontend"
        
        # Check if Node.js is installed
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js not found. Please install Node.js 18+ first.")
            return False
            
        # Create React app
        try:
            subprocess.run([
                "npx", "create-react-app", ".", "--template", "typescript"
            ], cwd=frontend_path, check=True)
            
            # Install additional dependencies
            subprocess.run([
                "npm", "install", 
                "react-router-dom", "react-query", "react-hook-form", 
                "react-hot-toast", "lucide-react", "axios"
            ], cwd=frontend_path, check=True)
            
            # Install dev dependencies
            subprocess.run([
                "npm", "install", "-D",
                "tailwindcss", "postcss", "autoprefixer",
                "@testing-library/jest-dom", "@testing-library/react", 
                "@testing-library/user-event"
            ], cwd=frontend_path, check=True)
            
            # Initialize Tailwind CSS
            subprocess.run(["npx", "tailwindcss", "init", "-p"], cwd=frontend_path, check=True)
            
            print("✅ React frontend created")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating React frontend: {e}")
            return False
    
    def create_config_files(self):
        """Create configuration files"""
        print("🔧 Creating configuration files...")
        
        # .env.example
        env_content = '''# Database Configuration
POSTGRES_DB=url_shortener
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Security
SECRET_KEY=your_very_secure_secret_key_here_at_least_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application URLs
BASE_URL=http://localhost:8000
REACT_APP_API_BASE_URL=http://localhost:8000

# Service Ports
URL_SERVICE_PORT=8001
USER_SERVICE_PORT=8002
ANALYTICS_SERVICE_PORT=8003
GATEWAY_PORT=8000
FRONTEND_PORT=3000
'''
        
        # docker-compose.yml
        docker_compose_content = '''version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-url_shortener}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
'''
        
        # Makefile
        makefile_content = '''.PHONY: help install test clean build up down

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run all tests"
	@echo "  build       Build Docker images"
	@echo "  up          Start services"
	@echo "  down        Stop services"
	@echo "  clean       Clean up"

install:
	@echo "Installing dependencies..."
	@cd frontend && npm install

up:
	@echo "Starting services..."
	@docker-compose up -d

down:
	@echo "Stopping services..."
	@docker-compose down

test:
	@echo "Running tests..."
	@cd frontend && npm test
'''
        
        # Write files
        (self.base_path / ".env.example").write_text(env_content)
        (self.base_path / "docker-compose.yml").write_text(docker_compose_content)
        (self.base_path / "Makefile").write_text(makefile_content)
        
        print("✅ Configuration files created")

def main():
    parser = argparse.ArgumentParser(description="FastAPI Project Generator")
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("--services", "-s", nargs="+", 
                       default=["url_service", "user_service", "analytics_service"],
                       help="List of microservices to create")
    parser.add_argument("--no-frontend", action="store_true", 
                       help="Skip React frontend creation")
    
    args = parser.parse_args()
    
    # Check if project directory already exists
    if Path(args.project_name).exists():
        print(f"❌ Directory '{args.project_name}' already exists!")
        sys.exit(1)
    
    # Create project
    generator = FastAPIProjectGenerator(args.project_name)
    
    try:
        # Create basic structure
        generator.create_project_structure()
        
        # Create microservices
        for service in args.services:
            generator.create_microservice(service)
        
        # Create API Gateway (always needed)
        print("🚪 Creating API Gateway...")
        gateway_path = generator.base_path / "backend/api_gateway"
        (gateway_path / "app/__init__.py").touch()
        (gateway_path / "tests/__init__.py").touch()
        
        # Create React frontend
        if not args.no_frontend:
            generator.create_react_frontend()
        
        # Create configuration files
        generator.create_config_files()
        
        print(f"""
🎉 Project '{args.project_name}' created successfully!

📁 Project structure:
{args.project_name}/
├── backend/
│   ├── api_gateway/
│   ├── services/
│   │   ├── {args.services[0] if args.services else 'url_service'}/
│   │   ├── {args.services[1] if len(args.services) > 1 else 'user_service'}/
│   │   └── {args.services[2] if len(args.services) > 2 else 'analytics_service'}/
│   └── shared/
├── frontend/
├── docker-compose.yml
├── .env.example
└── Makefile

🚀 Next steps:
1. cd {args.project_name}
2. cp .env.example .env
3. Edit .env with your configuration
4. make up (to start databases)
5. Start developing your services!

💡 Tips:
- Each service has its own virtual environment in venv/
- Use 'make help' to see available commands
- API docs will be available at http://localhost:800X/docs for each service
        """)
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()