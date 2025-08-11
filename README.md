# fast-react-project-generator
Similar to Django's startproject but for FastAPI microservices with react frontend. Here's how to use them:

1. Create the CLI Tools:
# Make them executable
chmod +x create_fastapi_project.py
chmod +x fastapi_service_generator.py

2. Create Your Project:
# Create the full Links From Liliput project
python create_fastapi_project.py <project-name>

# Or create with custom services
python create_fastapi_project.py <project-name> --services <service1> <service2> <service3> <service4>

3. Add Services Later:
# Navigate to your project
cd <project-name>

# Add a new service anytime
python ../fastapi_service_generator.py add-service <service1>
python ../fastapi_service_generator.py add-service <service2> --port 8005

🎯 What This Creates:
When you run python create_fastapi_project.py links_from_liliput, it automatically:
✅ Creates the complete directory structure
✅ Generates all FastAPI service files (main.py, config.py, routes, models, etc.)
✅ Creates React frontend using create-react-app
✅ Installs all dependencies (FastAPI, React packages, etc.)
✅ Sets up Docker configuration
✅ Creates .env.example and Makefile
✅ Initializes each service with proper structure

🛠️ Features of the CLI Tools:
Automatic port assignment for new services
Virtual environment setup for each microservice
Requirements.txt generation with all necessary packages
Docker configuration for each service
Test directory structure ready for pytest
Configuration management with Pydantic Settings
React integration with TypeScript support

📁 Generated Structure:
links_from_liliput/
├── backend/
│   ├── api_gateway/          # Auto-generated
│   ├── services/
│   │   ├── url_service/      # Port 8001
│   │   ├── user_service/     # Port 8002
│   │   └── analytics_service/ # Port 8003
│   └── shared/
├── frontend/                 # React app with all deps
├── docker-compose.yml        # Ready to use
├── .env.example             # All variables
└── Makefile                 # Dev commands

🎉 Start Developing:
bashcd <project-name>
cp .env.example .env          # Configure your environment
make up                       # Start databases
cd backend/services/url_service && source venv/bin/activate && python app/main.py

This gives you the same convenience as Django's startproject but for FastAPI microservices! Each service is properly structured and ready for development



-- At last if you want to git initialize the repo with readme and gitignore, run 
sh create_github_repo.sh
