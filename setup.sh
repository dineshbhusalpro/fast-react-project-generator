#!/bin/bash

echo "🛠️  Setting up FastAPI CLI tools..."

# Make scripts executable
chmod +x create_fastapi_project.py
chmod +x fastapi_service_generator.py

# Create symbolic links for global access (optional)
if command -v sudo &> /dev/null; then
    read -p "Install globally? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo ln -sf "$(pwd)/create_fastapi_project.py" /usr/local/bin/create-fastapi-project
        sudo ln -sf "$(pwd)/fastapi_service_generator.py" /usr/local/bin/fastapi-service
        echo "✅ Global installation complete!"
        echo "Use: create-fastapi-project <project_name>"
        echo "Use: fastapi-service add-service <service_name>"
    fi
fi

echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  python create_fastapi_project.py my_project"
echo "  python create_fastapi_project.py my_project --services url_service user_service"
echo "  python fastapi_service_generator.py add-service payment_service"