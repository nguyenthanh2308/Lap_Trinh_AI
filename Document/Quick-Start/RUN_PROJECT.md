# 🚀 Running the Project - Backend & Frontend

**Date:** 18/04/2026  
**Status:** ✅ Production Ready  
**Prerequisites:** See [INSTALLATION_GUIDE.md](../Setup/INSTALLATION_GUIDE.md)

---

## 📋 Quick Overview

This guide explains how to run both Backend (FastAPI) and Frontend (React) servers.

```
┌─────────────────────────────────────────────┐
│          Project Running Architecture        │
├─────────────────────────────────────────────┤
│                                              │
│  Frontend (React + Vite)                    │
│  http://localhost:5174                      │
│           ↓                                  │
│  [HTTP Requests (Axios)]                    │
│           ↓                                  │
│  Backend (FastAPI)                          │
│  http://localhost:8000                      │
│           ↓                                  │
│  [AI Model - Story Generation]              │
│           ↓                                  │
│  [Response JSON]                            │
│                                              │
└─────────────────────────────────────────────┘
```

---

## ⚡ Quick Start (30 seconds)

### **Terminal 1: Backend**
```powershell
cd "C:\Big_Data\AI\Final Term\BackEnd"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### **Terminal 2: Frontend**
```powershell
cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"
npx vite --host
```

### **Browser**
```
Open: http://localhost:5174
```

---

## 📖 Detailed Steps

### **Step 1: Start Backend Server**

#### **Option 1: Using PowerShell (Recommended)**

```powershell
# 1. Navigate to backend folder
cd "C:\Big_Data\AI\Final Term\BackEnd"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Start the server
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

**What this means:**
- ✅ Backend server is running
- ✅ Ready to receive API requests
- ✅ Reload enabled (code changes auto-reload)

#### **Option 2: Using Command Prompt (CMD)**

```cmd
cd C:\Big_Data\AI\Final Term\BackEnd
venv\Scripts\activate.bat
uvicorn app.main:app --reload
```

### **Step 2: Verify Backend is Running**

Open a new terminal and test the health endpoint:

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object StatusCode, Content

# Or using curl
curl http://localhost:8000/health

# Expected response:
# {"status":"ok"}
```

### **Step 3: Start Frontend Development Server**

**Open a NEW terminal** (keep backend running in previous terminal)

```powershell
# 1. Navigate to frontend folder
cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"

# 2. Start dev server
npx vite --host
```

**Expected output:**
```
VITE v8.0.8  ready in 234 ms

➜  Local:   http://localhost:5174/
➜  press h to show help
```

**What this means:**
- ✅ Frontend server is running
- ✅ Hot Module Replacement (HMR) enabled
- ✅ Code changes auto-reload in browser

### **Step 4: Open in Browser**

```
http://localhost:5174
```

**You should see:**
- 🎨 Beautiful story generator interface
- 📝 4 input fields for story parameters
- 🎯 Generate button
- 📖 Story display area

---

## 🧪 Testing the Application

### **Test 1: Generate a Story**

```
1. Fill in the form:
   - Character Name: "Minh"
   - Personality: "dũng cảm"
   - Setting: "một ngôi làng ven biển"
   - Theme: "phiêu lưu"

2. Click "Generate Story"

3. Watch the loading spinner

4. See the generated story appear

5. Click "Copy to Clipboard" to copy the story
```

### **Test 2: Form Validation**

```
1. Try clicking "Generate" with empty fields
   → Should show error: "All fields are required"

2. Try typing 101 characters in one field
   → Should show error: "Field cannot exceed 100 characters"

3. Fill form and click "Generate"
   → Should work normally
```

### **Test 3: Copy to Clipboard**

```
1. Generate a story

2. Click "Copy to Clipboard" button

3. Should show "Copied to clipboard!" message

4. Paste somewhere (Ctrl+V) to verify

5. Message auto-hides after 2 seconds
```

### **Test 4: Reset Form**

```
1. Fill form with data

2. Generate a story

3. Click "Reset" button

4. Form should clear
5. Story should be removed
```

---

## 🔌 API Testing (Advanced)

### **Using PowerShell**

```powershell
# Create JSON payload
$body = @{
    name = "Minh"
    personality = "dũng cảm"
    setting = "một ngôi làng ven biển"
    theme = "phiêu lưu"
} | ConvertTo-Json

# Send POST request
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/generate" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### **Using curl**

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Minh",
    "personality": "dũng cảm",
    "setting": "một ngôi làng ven biển",
    "theme": "phiêu lưu"
  }'
```

### **Using Postman**

1. Open Postman
2. Create new POST request
3. URL: `http://localhost:8000/api/v1/generate`
4. Body (JSON):
```json
{
  "name": "Minh",
  "personality": "dũng cảm",
  "setting": "một ngôi làng ven biển",
  "theme": "phiêu lưu"
}
```
5. Click Send
6. See response JSON

---

## 📊 Server Status & Monitoring

### **View Backend Logs**

The backend terminal shows:
```
INFO:     GET http://localhost:8000/health
INFO:     GET http://localhost:8000/
INFO:     POST http://localhost:8000/api/v1/generate
```

Each request shows:
- Request method (GET, POST)
- URL path
- Response status code

### **View Frontend Logs**

The frontend terminal shows:
```
[2:42:17 PM] [vite] ✓ /src/App.jsx updated
[2:42:17 PM] [vite] ✓ HMR update received
```

When you change code, it auto-reloads!

---

## 🛑 Stopping the Servers

### **Stop Backend**

In backend terminal:
```powershell
# Press Ctrl+C to stop
Ctrl+C

# Or close the terminal
```

### **Stop Frontend**

In frontend terminal:
```powershell
# Press Ctrl+C to stop
Ctrl+C

# Or close the terminal
```

---

## 🔄 Common Tasks

### **Change Backend Port**

```powershell
# Instead of:
uvicorn app.main:app --reload

# Run on different port (e.g., 8001):
uvicorn app.main:app --reload --port 8001

# Then update frontend .env:
# VITE_API_BASE_URL=http://localhost:8001
```

### **Change Frontend Port**

```powershell
# Instead of:
npx vite

### **Run Frontend Build**

```powershell
# Create production build
npm run build

# This creates optimized files in 'dist' folder
```

### **Run Backend Tests**

```powershell
cd "C:\Big_Data\AI\Final Term\BackEnd"
.\venv\Scripts\Activate.ps1
python test_endpoint.py
```

---

## 🐛 Troubleshooting

### **❌ Backend not starting**

```powershell
# Error: "ModuleNotFoundError: No module named 'fastapi'"
# Solution: Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Error: "Address already in use"
# Solution: Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### **❌ Frontend not starting**

```powershell
# Error: "npm: command not found"
# Solution: Make sure Node.js is installed
node --version

# Error: "Port 5174 already in use"
# Solution: Kill process
netstat -ano | findstr :5174
taskkill /PID <PID> /F
```

### **❌ API calls failing**

```powershell
# Check if backend is running:
curl http://localhost:8000/health

# Check browser console for errors:
# F12 → Console tab

# Verify CORS is enabled:
# Check backend console for CORS errors
```

### **❌ Hot reload not working**

```powershell
# Frontend changes not reflecting?
# Solution 1: Refresh browser (Ctrl+R)
# Solution 2: Restart dev server
# Solution 3: Clear browser cache (Ctrl+Shift+Del)
```

---

## 📈 Performance Tips

### **For Faster Story Generation**
- Use GPU if available (check with `torch.cuda.is_available()`)
- First generation is slower (model loading)
- Subsequent generations are faster

### **For Better Developer Experience**
- Keep terminals side-by-side
- Use VS Code integrated terminal
- Enable bracket colorization
- Use Prettier/ESLint extensions

### **For Production Deployment**
- Build frontend: `npm run build`
- Use Gunicorn for FastAPI: `gunicorn app.main:app`
- Use environment variables for secrets
- Enable HTTPS/SSL certificates

---

## 🎯 Complete Workflow Example

**Start fresh project (3 steps):**

```powershell
# Terminal 1: Backend
cd "C:\Big_Data\AI\Final Term\BackEnd"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2: Frontend (new terminal)
cd "C:\Big_Data\AI\Final Term\FrontEnd\story-generator"
npx vite --host

# Browser (3rd window)
# Open http://localhost:5174
# Fill form → Click Generate → See story!
```

**Total time from startup to usable app: ~10 seconds** ⚡

---

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| [INSTALLATION_GUIDE.md](../Setup/INSTALLATION_GUIDE.md) | How to install everything |
| [API/README.md](../API/README.md) | API endpoint documentation |
| [Frontend/VITE_SETUP_GUIDE.md](../Frontend/VITE_SETUP_GUIDE.md) | Frontend-specific setup |
| [Frontend/COMPONENT_GUIDE.md](../Frontend/COMPONENT_GUIDE.md) | Component documentation |

---

## ✅ Checklist Before Running

- [ ] Backend dependencies installed (43 packages)
- [ ] Frontend dependencies installed (181 packages)
- [ ] .env files configured (Backend & Frontend)
- [ ] Port 8000 & 5174 are available
- [ ] Python venv can be activated
- [ ] Node.js is installed

---

## 🎉 You're Ready!

Everything is set up and ready to run. Just:

1. **Start Backend** (Terminal 1)
2. **Start Frontend** (Terminal 2)
3. **Open Browser** to http://localhost:5174
4. **Generate Stories!** 🚀

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Backend won't start | Activate venv first |
| Frontend won't start | Check Node.js installed |
| Port already in use | Kill process with `taskkill` |
| API calls failing | Check backend console |
| Styles not loading | Clear browser cache |
| Changes not showing | Hard refresh (Ctrl+Shift+R) |

---

**Status:** ✅ **READY TO RUN**  
**Updated:** 18/04/2026  
**Time to run:** ~30 seconds setup + ~10 seconds startup  

Happy generating! 🎨✨
