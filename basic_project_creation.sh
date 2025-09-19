## create local folder with repo name
REPO_NAME='repo-name'

# Description
DESCRIPTION=REPO_NAME

# cd repo-folder
VISIBILITY='--public'

# create Readme.md
echo "# $REPO_NAME" > README.md

# create .gitignore
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

# Initialize, Stage and commit
git init
git add .
git commit -m "Repo Initialized"

# create repo
gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin --push --description "$DESCRIPTION"