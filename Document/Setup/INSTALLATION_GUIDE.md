# 📦 Complete Installation Guide - Backend & Frontend

**Date:** 18/04/2026  
**Status:** ✅ Production Ready  
**Tested On:** Windows 10/11, Python 3.8+, Node.js 18+

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before starting, make sure you have installed:

### **Required Software**
- ✅ **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
  ```powershell
  python --version
  ```

- ✅ **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
  ```powershell
  node --version
  npm --version
  ```

- ✅ **Git** - Download from [git-scm.com](https://git-scm.com/)
  ```powershell
  git --version
  ```

### **GPU Support (Optional)**
- ✅ **NVIDIA GPU** - For faster AI model inference
- ✅ **CUDA 11.8+** - Download from [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads)
- ✅ **cuDNN** - Download from [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)

*Note: The project will work on CPU too, but generation will be slower*

---

## 📁 Project Structure

```
C:\Big_Data\AI\Final Term\
│
├── BackEnd/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── story.py      # API endpoints
│   │   ├── models/
│   │   │   ├── model_loader.py   # AI model loading
│   │   │   └── schema.py         # Pydantic models
│   │   ├── utils/
│   │   │   └── helpers.py        # Helper functions
│   │   ├── config.py             # Configuration
│   │   └── main.py               # FastAPI app
│   ├── venv/                     # Virtual environment
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── .gitignore
│
├── FrontEnd/                      # React + Vite Frontend
│   ├── story-generator/
│   │   ├── src/
│   │   │   ├── components/        # React components
│   │   │   ├── hooks/             # Custom hooks
│   │   │   ├── services/          # API services
│   │   │   ├── App.jsx            # Main app
│   │   │   └── index.css          # Global styles
│   │   ├── public/                # Static files
│   │   ├── node_modules/          # Node dependencies
│   │   ├── package.json           # NPM config
│   │   ├── tailwind.config.js     # Tailwind setup
│   │   ├── vite.config.js         # Vite config
│   │   └── .env                   # Frontend config
│   └── .gitignore
│
└── Document/                      # Documentation
    ├── Setup/                     # Setup guides
    ├── Quick-Start/               # Quick start guides
    ├── Frontend/                  # Frontend docs
    ├── API/                       # API documentation
    └── ...
```

---

## 🔧 Backend Setup

### **Step 1: Navigate to Backend Directory**

```powershell
cd "C:\Big_Data\AI\Final Term\BackEnd"
```

### **Step 2: Create Virtual Environment**

```powershell
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\Activate.ps1
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
.\venv\Scripts\Activate.ps1
```

**Check activation:** Your prompt should show `(venv)` prefix

```powershell
# Example:
(venv) PS C:\Big_Data\AI\Final Term\BackEnd>
```

### **Step 3: Install Python Dependencies**

```powershell
# Make sure you're in venv
pip install --upgrade pip

# Install all dependencies (43 packages)
pip install -r requirements.txt
```

**This installs:**
- ✅ FastAPI 0.104.1
- ✅ Uvicorn 0.24.0 (ASGI server)
- ✅ PyTorch 2.1.1 (Deep learning)
- ✅ Transformers 4.36.0 (Hugging Face models)
- ✅ Pydantic 2.5.0 (Data validation)
- ✅ Python-dotenv (Environment variables)
- ✅ And 37 more packages

**Installation time:** 10-20 minutes (depends on GPU support)

### **Step 4: Configure Environment Variables**

```powershell
# Copy example to create .env
Copy-Item .env.example .env
```

**Edit .env if needed:**
```
# Models folder path (absolute or relative)
LOCAL_MODELS_PATH=./models

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# CORS settings
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

### **Step 5: Verify Backend Setup**

```powershell
# Still in venv, test import
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'GPU: {torch.cuda.is_available()}')"
```

**Expected output:**
```
PyTorch: 2.1.1
GPU: True  (or False if no GPU)
```

✅ **Backend Setup Complete!**

---

## 🎨 Frontend Setup

### **Step 1: Navigate to Frontend Directory**

```powershell
# Open new terminal (keep backend venv terminal open)
cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"
```

### **Step 2: Install Node Dependencies**

```powershell
# Install all npm packages
npm install
```

**This installs:**
- ✅ React 19.2.5
- ✅ Vite 8.0.8
- ✅ Tailwind CSS 4.2.2
- ✅ Axios 1.15.0
- ✅ Lucide React 1.8.0
- ✅ And 11 more packages

**Installation time:** 2-5 minutes

**Check installation:**
```powershell
npm list
```

### **Step 3: Configure Environment Variables**

```powershell
# .env file should already exist
# Verify it has:
cat .env
```

**Expected content:**
```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=AI Story Generator
VITE_APP_VERSION=1.0.0
```

**If .env is missing, create it:**
```powershell
@"
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=AI Story Generator
VITE_APP_VERSION=1.0.0
"@ | Out-File -Encoding UTF8 .env
```

### **Step 4: Verify Frontend Setup**

```powershell
# Check Tailwind
npm list tailwindcss

# Check Vite
npm list vite

# List all dependencies
npm list --depth=0
```

**Expected output:**
```
├── axios@1.15.0
├── lucide-react@1.8.0
├── react@19.2.5
├── react-dom@19.2.5
├── tailwindcss@4.2.2
├── vite@8.0.8
└── ...
```

✅ **Frontend Setup Complete!**

---

## ✅ Verification Checklist

### **Backend Verification**

```powershell
# 1. Navigate to backend
cd "C:\Big_Data\AI\Final Term\BackEnd"

# 2. Activate venv
.\venv\Scripts\Activate.ps1

# 3. Check Python packages
pip list | grep -E "fastapi|torch|transformers"

# Output should show:
# fastapi          0.104.1
# torch            2.1.1
# transformers     4.36.0
```

### **Frontend Verification**

```powershell
# 1. Navigate to frontend
cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"

# 2. Check Node packages
npm list | grep -E "react|vite|tailwindcss"

# Output should show versions
```

### **Project Files Verification**

```powershell
# Backend files
Test-Path "C:\Big_Data\AI\Final Term\BackEnd\app\main.py"
Test-Path "C:\Big_Data\AI\Final Term\BackEnd\requirements.txt"
Test-Path "C:\Big_Data\AI\Final Term\BackEnd\venv"

# Frontend files
Test-Path "C:\Big_Data\AI\Final Term\FrontEnd\story-generator\src"
Test-Path "C:\Big_Data\AI\Final Term\FrontEnd\story-generator\package.json"
Test-Path "C:\Big_Data\AI\Final Term\FrontEnd\story-generator\node_modules"
```

**All should return `True` ✅**

---

## 🚀 Next Steps

After completing the installation:

1. **Start Backend Server**
   ```powershell
   cd "C:\Big_Data\AI\Final Term\BackEnd"
   .\venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload
   ```
   → Runs at `http://localhost:8000`

2. **Start Frontend Dev Server**
   ```powershell
   cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"
   npm run dev
   ```
   → Runs at `http://localhost:5174`

3. **Open Browser**
   - Open `http://localhost:5174` in your browser
   - You should see the Story Generator interface

4. **Test Story Generation**
   - Fill in the 4 form fields
   - Click "Generate Story"
   - Watch the AI create your story!

📖 See **RUN_PROJECT.md** in Quick-Start folder for detailed running instructions.

---

## 🔧 Troubleshooting

### **Python Issues**

#### ❌ "Python command not found"
```powershell
# Make sure Python is in PATH
python --version

# If not found, add Python to PATH manually or reinstall
```

#### ❌ "venv activation fails"
```powershell
# Try execution policy fix
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
```

#### ❌ "pip install fails"
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

#### ❌ "PyTorch not found after install"
```powershell
# Restart PowerShell/terminal after installation
# Or restart Python kernel in IDE

# Test installation
python -c "import torch; print(torch.__version__)"
```

### **Node.js Issues**

#### ❌ "npm command not found"
```powershell
# Verify Node.js installation
node --version
npm --version

# If not found, reinstall Node.js
```

#### ❌ "npm install fails"
```powershell
# Clear npm cache
npm cache clean --force

# Try install again
npm install

# If still fails, delete node_modules and try again
Remove-Item -Recurse -Force node_modules
npm install
```

#### ❌ "Port 5173/5174 already in use"
```powershell
# Find process using port
netstat -ano | findstr :5173

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Try running dev server again
npm run dev
```

### **Git Issues**

#### ❌ "Git not found"
```powershell
git --version

# If not found, install from git-scm.com
```

#### ❌ "Permission denied when pushing"
```powershell
# Configure Git
git config --global user.email "your@email.com"
git config --global user.name "Your Name"

# Try pushing again
git push
```

---

## 📊 Installation Summary

| Component | Time | Packages | Size |
|-----------|------|----------|------|
| Backend (Python) | 10-20 min | 43 | ~2GB (with PyTorch) |
| Frontend (Node) | 2-5 min | 181 | ~500MB |
| **Total** | **15-25 min** | **224** | **~2.5GB** |

---

## 🎯 Final Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Backend venv created and activated
- [ ] 43 Python packages installed
- [ ] .env file configured (Backend)
- [ ] 181 Node packages installed
- [ ] .env file configured (Frontend)
- [ ] All verification checks passed
- [ ] Ready to run (see RUN_PROJECT.md)

---

## 📚 Related Documentation

- **Setup/README.md** - Setup folder overview
- **Quick-Start/RUN_PROJECT.md** - How to run the project
- **Frontend/VITE_SETUP_GUIDE.md** - Detailed frontend setup
- **API/README.md** - API documentation

---

## 📞 Support

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Read related documentation in Document/ folder
3. Check error messages carefully for clues
4. Verify all prerequisites are installed
5. Try restarting terminals/IDEs

---

**Status:** ✅ **INSTALLATION GUIDE COMPLETE**  
**Updated:** 18/04/2026  
**For:** Windows 10/11 with Python 3.8+ and Node.js 18+  

Next: Open **RUN_PROJECT.md** to start the project! 🚀
