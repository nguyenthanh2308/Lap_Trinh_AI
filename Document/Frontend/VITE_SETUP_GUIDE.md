# 🚀 Vite + React + Tailwind CSS Setup Guide

**Project:** AI-Powered Short Story Generator Frontend  
**Tech Stack:** Vite, React, Tailwind CSS, Axios, Lucide React  
**Date:** 18/04/2026

---

## 📋 Table of Contents

1. [Quick Start Commands](#quick-start-commands)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Folder Structure](#folder-structure)
4. [Configuration Files](#configuration-files)
5. [Verification & Testing](#verification--testing)
6. [Next Steps](#next-steps)

---

## ⚡ Quick Start Commands

```bash
# 1. Create Vite project with React
npm create vite@latest story-generator-fe -- --template react

# 2. Navigate to project
cd story-generator-fe

# 3. Install dependencies
npm install

# 4. Install Tailwind CSS and PostCSS
npm install -D tailwindcss postcss autoprefixer

# 5. Initialize Tailwind
npx tailwindcss init -p

# 6. Install Axios and Lucide React
npm install axios lucide-react

# 7. Start development server
npm run dev
```

---

## 📝 Step-by-Step Setup

### Step 1: Create Vite Project

#### Command
```powershell
npm create vite@latest story-generator-fe -- --template react
```

#### What This Does
- Creates new Vite project with React template
- Sets up build configuration
- Creates package.json with react and react-dom dependencies

#### Expected Output
```
✔ Project name: story-generator-fe
✔ Using template: react
✔ Scaffolding project in story-generator-fe...

Done. Now run:
  cd story-generator-fe
  npm install
  npm run dev
```

#### Next
```powershell
cd story-generator-fe
```

---

### Step 2: Install Dependencies

#### Command
```powershell
npm install
```

#### What This Does
- Installs all dependencies from package.json
- Creates node_modules folder
- Generates package-lock.json

#### Dependencies Installed
- `react` - React library
- `react-dom` - React DOM rendering
- `vite` - Build tool
- `@vitejs/plugin-react` - Vite React plugin

#### Verify Installation
```powershell
npm list
```

---

### Step 3: Install Tailwind CSS

#### Command
```powershell
npm install -D tailwindcss postcss autoprefixer
```

#### What This Does
- Installs Tailwind CSS (dev dependency)
- Installs PostCSS (CSS processor)
- Installs Autoprefixer (CSS vendor prefix tool)

#### Dependencies
```json
{
  "devDependencies": {
    "tailwindcss": "^3.3.x",
    "postcss": "^8.4.x",
    "autoprefixer": "^10.4.x"
  }
}
```

---

### Step 4: Initialize Tailwind Configuration

#### Command
```powershell
npx tailwindcss init -p
```

#### What This Creates

**A. `tailwind.config.js`** - Tailwind configuration
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**B. `postcss.config.js`** - PostCSS configuration
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

#### What These Do
- `tailwind.config.js` - Tells Tailwind which files to scan for class names
- `postcss.config.js` - Configures CSS processing pipeline

---

### Step 5: Configure Tailwind in CSS

#### File: `src/index.css`

Replace entire content with:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### What This Does
- Injects Tailwind's base styles (resets)
- Injects component classes
- Injects utility classes
- Makes all Tailwind classes available

#### Verify
```css
/* After build, this will be expanded to thousands of CSS lines */
```

---

### Step 6: Install Axios and Lucide React

#### Command
```powershell
npm install axios lucide-react
```

#### Dependencies Added

**A. Axios** - HTTP client
```json
"axios": "^1.6.x"
```

**Purpose:**
- Make API requests to backend
- Handle request/response interceptors
- Type-safe with TypeScript support

**B. Lucide React** - Icon library
```json
"lucide-react": "^0.x"
```

**Purpose:**
- Beautiful, consistent icons
- Tree-shakeable (imports only used icons)
- Easy to customize (color, size, stroke)

#### Usage Examples

**Axios:**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

const response = await api.post('/api/v1/generate', {
  name: 'Minh',
  personality: 'dũng cảm',
  setting: 'một ngôi làng ven biển',
  theme: 'phiêu lưu'
});
```

**Lucide React:**
```javascript
import { Sparkles, Copy, RefreshCw } from 'lucide-react';

function GenerateButton() {
  return (
    <button>
      <Sparkles size={20} className="mr-2" />
      Generate Story
    </button>
  );
}
```

---

### Step 7: Start Development Server

#### Command
```powershell
npm run dev
```

#### Output
```
  VITE v4.x.x  ready in xxxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### What Happens
- Starts local development server
- Hot Module Replacement (HMR) enabled
- Auto-refreshes browser on code changes
- Accessible at http://localhost:5173

#### Access Frontend
Open browser: http://localhost:5173

---

## 📁 Folder Structure

### Recommended Structure
```
story-generator-fe/
├── src/
│   ├── components/
│   │   ├── StoryForm.jsx           ← Story input form
│   │   ├── StoryDisplay.jsx        ← Generated story display
│   │   ├── Header.jsx              ← App header
│   │   ├── Footer.jsx              ← App footer
│   │   ├── LoadingSpinner.jsx      ← Loading indicator
│   │   └── index.js                ← Component exports
│   │
│   ├── services/
│   │   ├── api.js                  ← Axios configuration
│   │   ├── storyService.js         ← API calls for stories
│   │   └── index.js                ← Service exports
│   │
│   ├── hooks/
│   │   ├── useStory.js             ← Story generation hook
│   │   ├── useApi.js               ← API call hook
│   │   └── index.js                ← Hook exports
│   │
│   ├── assets/
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── styles/
│   │   ├── index.css               ← Global styles + Tailwind
│   │   └── variables.css           ← CSS variables
│   │
│   ├── utils/
│   │   ├── constants.js            ← Constants
│   │   ├── formatters.js           ← Data formatters
│   │   └── validators.js           ← Input validators
│   │
│   ├── App.jsx                     ← Main app component
│   ├── App.css                     ← App styles
│   └── main.jsx                    ← Entry point
│
├── public/
│   ├── favicon.ico
│   └── robots.txt
│
├── index.html                      ← HTML entry point
├── vite.config.js                  ← Vite configuration
├── tailwind.config.js              ← Tailwind configuration
├── postcss.config.js               ← PostCSS configuration
├── package.json                    ← Dependencies
├── package-lock.json               ← Dependency lock file
├── .gitignore                      ← Git ignore rules
└── README.md                       ← Project documentation
```

### Folder Descriptions

| Folder | Purpose |
|--------|---------|
| `src/components/` | Reusable React components |
| `src/services/` | API calls and external services |
| `src/hooks/` | Custom React hooks |
| `src/assets/` | Images, fonts, static files |
| `src/styles/` | Global and shared CSS |
| `src/utils/` | Helper functions and constants |
| `public/` | Static files served directly |

---

## ⚙️ Configuration Files

### A. `vite.config.js`

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: false,
    open: true
  }
})
```

**Key Settings:**
- `port: 5173` - Development server port
- `strictPort: false` - Try different port if 5173 in use
- `open: true` - Auto-open browser on npm run dev

### B. `tailwind.config.js` (Already created)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

**Customization:**
- Add custom colors under `theme.extend.colors`
- Add custom fonts under `theme.extend.fontFamily`
- Add plugins under `plugins: []`

### C. `postcss.config.js` (Already created)

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### D. `package.json` (Scripts Section)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx"
  }
}
```

**Scripts:**
- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Check code quality

---

## 🛠️ Essential Service Files

### A. `src/services/api.js`

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
```

### B. `src/services/storyService.js`

```javascript
import api from './api';

export const storyService = {
  generateStory: async (storyData) => {
    try {
      const response = await api.post('/api/v1/generate', {
        name: storyData.name,
        personality: storyData.personality,
        setting: storyData.setting,
        theme: storyData.theme,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};
```

### C. `src/hooks/useStory.js`

```javascript
import { useState } from 'react';
import { storyService } from '../services/storyService';

export const useStory = () => {
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateStory = async (storyData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await storyService.generateStory(storyData);
      setStory(result.story);
      return result;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate story');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    story,
    loading,
    error,
    generateStory,
  };
};
```

---

## ✅ Verification & Testing

### 1. Verify Installation

```powershell
# Check Node.js version
node --version  # Should be v16 or higher

# Check npm version
npm --version   # Should be v8 or higher

# List installed packages
npm list
```

**Expected:**
```
story-generator-fe@0.0.0
├── react@18.x.x
├── react-dom@18.x.x
├── axios@1.x.x
├── lucide-react@0.x.x
├── tailwindcss@3.x.x (dev)
└── ...
```

### 2. Test Development Server

```powershell
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Browser Check:**
- Open http://localhost:5173
- Should see Vite + React welcome screen
- Make changes to src/App.jsx
- Browser should hot-reload

### 3. Test Build Process

```powershell
npm run build
```

**Expected:**
```
vite v4.x.x building for production...
✓ 1,234 modules transformed.
dist/index.html                    1.23 kb │ gzip: 0.45 kb
dist/assets/index-abc123.js        456.78 kb │ gzip: 121.23 kb
✓ build complete in 10s
```

### 4. Test Production Preview

```powershell
npm run preview
```

**Expected:**
```
  ➜  Local:   http://localhost:4173/
```

---

## 📦 Environment Variables

### Create `.env` file

```bash
# Backend API
VITE_API_BASE_URL=http://localhost:8000

# App settings
VITE_APP_TITLE=AI Story Generator
VITE_APP_VERSION=1.0.0
```

### Access in Code

```javascript
// In React components
const apiUrl = import.meta.env.VITE_API_BASE_URL;
const appTitle = import.meta.env.VITE_APP_TITLE;

// For production, use .env.production
// VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## 🎨 Example Component: StoryForm

```javascript
// src/components/StoryForm.jsx
import { useState } from 'react';
import { Sparkles } from 'lucide-react';

export function StoryForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    name: '',
    personality: '',
    setting: '',
    theme: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Character Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          maxLength="100"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., Minh"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Personality</label>
        <input
          type="text"
          name="personality"
          value={formData.personality}
          onChange={handleChange}
          maxLength="100"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., dũng cảm"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Setting</label>
        <input
          type="text"
          name="setting"
          value={formData.setting}
          onChange={handleChange}
          maxLength="100"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., một ngôi làng ven biển"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Theme</label>
        <input
          type="text"
          name="theme"
          value={formData.theme}
          onChange={handleChange}
          maxLength="100"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., phiêu lưu"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition"
      >
        <Sparkles size={20} />
        {loading ? 'Generating...' : 'Generate Story'}
      </button>
    </form>
  );
}
```

---

## 🚀 Next Steps

### 1. Create Project Structure
```powershell
# Create folders manually or use commands
mkdir src/components
mkdir src/services
mkdir src/hooks
mkdir src/utils
mkdir src/assets/images
mkdir src/styles
```

### 2. Create Service Files
- Copy `api.js` to `src/services/`
- Copy `storyService.js` to `src/services/`
- Copy `useStory.js` hook to `src/hooks/`

### 3. Build Components
- `StoryForm.jsx` - Input form
- `StoryDisplay.jsx` - Display generated story
- `Header.jsx` - Navigation
- `LoadingSpinner.jsx` - Loading indicator

### 4. Create Main App Layout
```javascript
// src/App.jsx
import { useState } from 'react';
import { StoryForm } from './components/StoryForm';
import { StoryDisplay } from './components/StoryDisplay';
import { useStory } from './hooks/useStory';

export default function App() {
  const { story, loading, error, generateStory } = useStory();

  const handleGenerateStory = async (formData) => {
    try {
      await generateStory(formData);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-center mb-12">AI Story Generator</h1>
        
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <StoryForm onSubmit={handleGenerateStory} loading={loading} />
          </div>
          
          <div>
            <StoryDisplay story={story} loading={loading} error={error} />
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 5. Test API Connection
- Start backend: `uvicorn app.main:app --reload`
- Start frontend: `npm run dev`
- Try generating a story
- Check browser console for API calls

### 6. Deploy
- Build: `npm run build`
- Deploy `dist/` folder to hosting
- Update `VITE_API_BASE_URL` for production

---

## 📚 Useful Commands Summary

```powershell
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build

# Package Management
npm install             # Install dependencies
npm install <package>   # Install new package
npm update              # Update packages
npm audit               # Check security issues

# Utilities
npm run lint            # Check code quality (if configured)
npm start               # Start production server

# Cleaning
npm cache clean --force # Clear npm cache
rm -r node_modules      # Remove node_modules (on Windows: rmdir /s node_modules)
rm package-lock.json    # Remove lock file
npm install             # Reinstall everything
```

---

## 🔗 Useful Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [Axios Documentation](https://axios-http.com/)
- [Lucide Icons](https://lucide.dev/)

---

## ✨ Common Issues & Solutions

### Issue 1: Port 5173 Already in Use
```powershell
# Change port in vite.config.js
server: {
  port: 5174,
  strictPort: false
}
```

### Issue 2: CORS Errors
```javascript
// Backend should have CORS enabled
# Check that backend has:
app.add_middleware(CORSMiddleware, ...)

# Verify CORS origins include http://localhost:5173
```

### Issue 3: Tailwind Styles Not Applied
```bash
# Ensure postcss.config.js exists
# Ensure tailwind.config.js content paths are correct
# Run: npm run build to trigger PostCSS processing
```

### Issue 4: Hot Reload Not Working
```powershell
# Check vite.config.js has react plugin
# Restart dev server: npm run dev
# Clear browser cache (Ctrl+Shift+Del)
```

---

## 🎯 Checklist

- [ ] Node.js installed (v16+)
- [ ] npm installed (v8+)
- [ ] Vite project created
- [ ] Dependencies installed
- [ ] Tailwind CSS configured
- [ ] Axios installed
- [ ] Lucide React installed
- [ ] Folder structure created
- [ ] Services configured
- [ ] Hooks created
- [ ] Dev server running
- [ ] Backend API running on port 8000
- [ ] CORS enabled on backend

---

## 📞 Support

If you encounter issues:
1. Check the error message in browser console
2. Check backend console for API errors
3. Verify backend is running: `http://localhost:8000/health`
4. Check network tab in browser DevTools
5. Review `.env` file configuration

---

**Status:** ✅ Ready to build!  
**Next:** Start creating your React components and styling with Tailwind CSS 🎨

