#!/usr/bin/env bash
set -e

# Ask for repo name
read -p "Enter repository name: " REPO_NAME

# Check if the repo already exists on GitHub
if gh repo view "$REPO_NAME" &>/dev/null; then
    echo "❌ Repository '$REPO_NAME' already exists on GitHub."
    exit 1
fi

# Ask for visibility
read -p "Should the repository be private? (y/n): " PRIVATE_ANSWER
if [[ "$PRIVATE_ANSWER" =~ ^[Yy]$ ]]; then
    VISIBILITY="--private"
else
    VISIBILITY="--public"
fi

# Ask for description
read -p "Enter repository description (optional): " DESCRIPTION

# Ask if you want to initialize with README
read -p "Initialize with README.md? (y/n): " README_ANSWER
if [[ "$README_ANSWER" =~ ^[Yy]$ ]]; then
    INIT_README=true
else
    INIT_README=false
fi

# Create local directory only if it doesn't exist
if [[ ! -d "$REPO_NAME" ]]; then
    mkdir "$REPO_NAME"
    echo "Created directory $REPO_NAME"
else
    echo "✅ Local folder '$REPO_NAME' already exists"
fi

cd "$REPO_NAME"

# Initialize Git if not already
if [[ ! -d ".git" ]]; then
    git init
    echo "Initialized git repository"
else
    echo "✅ Git already initialized"
fi

# Optionally create README
if [[ "$INIT_README" = true && ! -f README.md ]]; then
    echo "# $REPO_NAME" > README.md
fi

# Create .gitignore if not exists
if [[ ! -f .gitignore ]]; then
    cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pdb
.env
.env.*

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React build
/build

# Docker
*.pid
*.log
docker-compose.override.yml

# IDE/Editor
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF
    echo "Created .gitignore"
fi

# Stage and commit
git add .
git commit -m "Initial commit" || echo "Nothing to commit yet"

# Create repo on GitHub
if [[ -n "$DESCRIPTION" ]]; then
    gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin --push --description "$DESCRIPTION"
else
    gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin --push
fi

echo "🎉 Repository '$REPO_NAME' created and pushed to GitHub!"
