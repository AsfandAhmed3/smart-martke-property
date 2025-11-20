# 🍎 MacBook Setup Guide - Smart Property Manager

Complete setup instructions for macOS with and without Homebrew.

---

## Table of Contents
- [Method 1: Setup WITH Homebrew (Recommended)](#method-1-setup-with-homebrew-recommended)
- [Method 2: Setup WITHOUT Homebrew (Manual)](#method-2-setup-without-homebrew-manual)
- [Project Setup (Common for Both Methods)](#project-setup-common-for-both-methods)
- [VS Code Configuration](#vs-code-configuration)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

---

# Method 1: Setup WITH Homebrew (Recommended)

Homebrew is the most popular package manager for macOS. It simplifies installation and management of development tools.

## Step 1: Install Homebrew

Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, follow the instructions to add Homebrew to your PATH. You'll need to run something like:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify Homebrew installation:
```bash
brew --version
```

## Step 2: Install Python 3.11+

```bash
brew install python@3.11
python3 --version
```

## Step 3: Install Node.js & npm

```bash
brew install node
node --version
npm --version
```

## Step 4: Install Git

```bash
brew install git
git --version
```

## Step 5: Install PostgreSQL (Optional - for production)

```bash
brew install postgresql@15
brew services start postgresql@15
```

## Advantages of Using Homebrew
- ✅ Easy updates: `brew upgrade`
- ✅ Easy uninstall: `brew uninstall <package>`
- ✅ Dependency management
- ✅ Community support
- ✅ One-command installations

---

# Method 2: Setup WITHOUT Homebrew (Manual)

If you prefer not to use Homebrew, you can install everything manually.

## Step 1: Install Python 3.11+

### Option A: Download from Python.org
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 or newer for macOS
3. Run the `.pkg` installer
4. Follow installation wizard
5. Verify installation:
```bash
python3 --version
```

### Option B: Use Xcode Command Line Tools
```bash
xcode-select --install
python3 --version
```

## Step 2: Install Node.js & npm

1. Visit https://nodejs.org/
2. Download the **LTS version** for macOS (`.pkg` installer)
3. Run the installer
4. Follow installation steps
5. Verify installation:
```bash
node --version
npm --version
```

## Step 3: Install Git

### Option A: Xcode Command Line Tools (includes Git)
```bash
xcode-select --install
git --version
```

### Option B: Download from Official Site
1. Visit https://git-scm.com/download/mac
2. Download the installer
3. Run and follow instructions
4. Verify:
```bash
git --version
```

## Step 4: PostgreSQL (Optional)

1. Visit https://www.postgresql.org/download/macosx/
2. Download Postgres.app or the installer
3. Follow installation instructions

---

# Project Setup (Common for Both Methods)

After installing prerequisites using either method, follow these steps:

## Step 1: Get Project Files

### Option A: Clone from GitHub
```bash
cd ~/Desktop
git clone https://github.com/YOUR_USERNAME/smart-property-manager.git
cd smart-property-manager
```

### Option B: Copy from USB/Drive
```bash
# Copy the project folder to your Mac
# Then navigate to it
cd ~/Desktop/smart-property-manager
# or
cd ~/Documents/smart-property-manager
```

## Step 2: Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
# You should see (venv) prefix in your terminal

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# If installation fails, install packages individually:
# pip install django==4.2.26
# pip install djangorestframework==3.16.1
# pip install djangorestframework-simplejwt==5.5.1
# pip install django-cors-headers==4.6.0
# pip install django-filter==25.0
# pip install python-dotenv
# pip install Pillow
# pip install psycopg2-binary

# Create environment file (optional)
cp .env.example .env
# Edit .env with your settings if needed

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superadmin user
python manage.py create_superadmin \
  --email="admin@smartproperty.com" \
  --password="admin123456" \
  --first-name="Super" \
  --last-name="Admin"

# Start Django development server
python manage.py runserver
```

**Backend runs on:** http://127.0.0.1:8000

✅ **Keep this terminal window open!**

## Step 3: Frontend Setup (Vue.js)

**Open a NEW Terminal tab/window** (Cmd + T):

```bash
# Navigate to frontend directory
cd ~/Desktop/smart-property-manager/frontend
# Adjust path to where your project is located

# Install npm dependencies
npm install

# If installation is slow or fails, try:
npm install --legacy-peer-deps

# Or clean cache first:
npm cache clean --force
npm install

# Create environment file (optional)
cp .env.example .env

# Start Vue development server
npm run dev
```

**Frontend runs on:** http://localhost:5173

✅ **Keep this terminal window open too!**

---

# VS Code Configuration

## Step 1: Open Project in VS Code

```bash
cd ~/Desktop/smart-property-manager
code .
```

If `code` command doesn't work:
1. Open VS Code manually
2. Go to: **File → Open Folder**
3. Select `smart-property-manager` folder

## Step 2: Install VS Code Extensions (Recommended)

Press `Cmd + Shift + X` to open Extensions, then install:

### Essential Extensions:
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- **Vue - Official** (by Vue)
- **ESLint** (by Microsoft)

### Optional but Helpful:
- **Prettier - Code formatter**
- **Auto Rename Tag**
- **Path Intellisense**
- **GitLens**
- **Better Comments**
- **Bracket Pair Colorizer**

## Step 3: Configure Python Interpreter

1. Open Command Palette: `Cmd + Shift + P`
2. Type: `Python: Select Interpreter`
3. Select: `./backend/venv/bin/python3`

Or click the Python version in the bottom-right corner of VS Code.

## Step 4: Create Workspace Settings

Create `.vscode/settings.json` in project root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.analysis.extraPaths": [
    "${workspaceFolder}/backend"
  ],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.DS_Store": true,
    "**/node_modules": true
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "[vue]": {
    "editor.defaultFormatter": "Vue.volar"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Step 5: Using Integrated Terminal

1. Open terminal: `` Ctrl + ` ``
2. Click `+` icon to create multiple terminals
3. Use split view for backend and frontend

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

# Running the Application

## Daily Startup Process

### Terminal 1 - Backend:
```bash
cd ~/Desktop/smart-property-manager/backend
source venv/bin/activate
python manage.py runserver
```

### Terminal 2 - Frontend:
```bash
cd ~/Desktop/smart-property-manager/frontend
npm run dev
```

## Access the Application

1. **Frontend Application:** http://localhost:5173
2. **Backend API:** http://127.0.0.1:8000/api/
3. **Django Admin Panel:** http://127.0.0.1:8000/admin/

## Default Login Credentials

```
Email: admin@smartproperty.com
Password: admin123456
```

## Stopping the Servers

Press `Ctrl + C` in each terminal window to stop the servers.

---

# Automated Start Script (Optional)

Create `start.sh` in project root:

```bash
#!/bin/bash

echo "🚀 Starting Smart Property Manager..."
echo ""

# Start backend
echo "📦 Starting Backend Server..."
cd backend
source venv/bin/activate
python manage.py runserver > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to initialize
sleep 3

# Start frontend
echo "🎨 Starting Frontend Server..."
cd frontend
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servers Started Successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Backend:  http://127.0.0.1:8000"
echo "📍 Frontend: http://localhost:5173"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"

# Trap Ctrl+C to kill both processes
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Servers stopped'; exit" INT

# Wait indefinitely
wait
```

Make it executable and run:
```bash
chmod +x start.sh
./start.sh
```

---

# Troubleshooting

## Common Issues on Mac

### Issue: "python: command not found"
**Solution:** Use `python3` instead
```bash
python3 --version
python3 manage.py runserver
```

### Issue: "pip: command not found"
**Solution:** Use `python3 -m pip`
```bash
python3 -m pip install -r requirements.txt
```

### Issue: Permission denied during installation
**Solution:** Use `--user` flag or ensure virtual environment is activated
```bash
pip install --user -r requirements.txt
# OR (preferred)
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port 8000 or 5173 already in use
**Solution:** Kill the process using the port
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Issue: npm install fails or is very slow
**Solution:** Try these steps in order
```bash
# 1. Clean npm cache
npm cache clean --force

# 2. Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# 3. Reinstall with legacy peer deps
npm install --legacy-peer-deps

# 4. If still failing, try installing globally first
npm install -g npm@latest
npm install
```

### Issue: "xcrun: error: invalid active developer path"
**Solution:** Install Xcode Command Line Tools
```bash
xcode-select --install
```

### Issue: Virtual environment activation not working
**Solution:** Check shell and activation script
```bash
# For zsh (default on new Macs)
source venv/bin/activate

# If using bash
source venv/bin/activate

# If using fish shell
source venv/bin/activate.fish

# Verify activation - you should see (venv) in prompt
which python
```

### Issue: Module not found errors in Python
**Solution:** Ensure virtual environment is activated and dependencies installed
```bash
# Make sure you see (venv) in terminal prompt
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Issue: Database migration errors
**Solution:** Reset database
```bash
cd backend
source venv/bin/activate

# Delete database
rm db.sqlite3

# Delete migration files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Recreate superadmin
python manage.py create_superadmin \
  --email="admin@smartproperty.com" \
  --password="admin123456" \
  --first-name="Super" \
  --last-name="Admin"
```

### Issue: CORS errors in browser console
**Solution:** Check backend CORS configuration
1. Ensure `django-cors-headers` is installed
2. Verify `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`
3. Should include: `http://localhost:5173`

### Issue: VS Code Python linting errors
**Solution:** Select correct interpreter
```bash
# In VS Code:
# Cmd + Shift + P
# Type: Python: Select Interpreter
# Choose: ./backend/venv/bin/python3
```

### Issue: .DS_Store files everywhere
**Solution:** Add to .gitignore (already done) and clean existing
```bash
# Remove all .DS_Store files
find . -name ".DS_Store" -delete

# Prevent macOS from creating them on network drives
defaults write com.apple.desktopservices DSDontWriteNetworkStores true
```

---

# Database Reset (Clean Start)

If you need to completely reset the database:

```bash
cd backend
source venv/bin/activate

# Step 1: Delete database file
rm db.sqlite3

# Step 2: Delete all migration files except __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Step 3: Create fresh migrations
python manage.py makemigrations

# Step 4: Apply migrations
python manage.py migrate

# Step 5: Create superadmin
python manage.py create_superadmin \
  --email="admin@smartproperty.com" \
  --password="admin123456" \
  --first-name="Super" \
  --last-name="Admin"

# Step 6: Run server
python manage.py runserver
```

---

# Update Dependencies

## Update Python Packages
```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## Update Node Packages
```bash
cd frontend
npm update
# or for major updates
npm install -g npm-check-updates
ncu -u
npm install
```

---

# Verification Checklist

Before starting development, verify:

- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (`git --version`)
- [ ] Virtual environment created (`backend/venv/` exists)
- [ ] Backend dependencies installed (no errors)
- [ ] Frontend dependencies installed (`node_modules/` exists)
- [ ] Database migrations applied
- [ ] Superadmin user created
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 5173
- [ ] Can access http://localhost:5173
- [ ] Can login with admin credentials
- [ ] No CORS errors in browser console

---

# Quick Reference Commands

## Virtual Environment
```bash
# Activate
source backend/venv/bin/activate

# Deactivate
deactivate

# Verify activation
which python  # Should show path to venv
```

## Django Commands
```bash
# Run server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## Vue/Vite Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

---

# Mac-Specific Productivity Tips

1. **Spotlight Search:** `Cmd + Space` to quickly open Terminal or VS Code
2. **Mission Control:** Swipe up with 3-4 fingers to see all windows
3. **Split View:** Drag window to edge to snap it to half screen
4. **Terminal Tabs:** `Cmd + T` for new tab, `Cmd + W` to close
5. **VS Code Terminal:** `` Ctrl + ` `` to toggle terminal
6. **Force Quit:** `Cmd + Option + Esc` if app freezes
7. **Screenshot:** `Cmd + Shift + 4` for selection screenshot

---

# Environment Variables

Create `backend/.env` file for sensitive data:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
DB_NAME=smart_property
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

Create `frontend/.env` file:

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Smart Property Manager
```

---

# Need Help?

- **Django Documentation:** https://docs.djangoproject.com/
- **Vue.js Documentation:** https://vuejs.org/guide/
- **Vite Documentation:** https://vitejs.dev/guide/
- **Python Documentation:** https://docs.python.org/3/
- **Node.js Documentation:** https://nodejs.org/docs/

---

**✅ Setup Complete! Happy Coding! 🚀**
