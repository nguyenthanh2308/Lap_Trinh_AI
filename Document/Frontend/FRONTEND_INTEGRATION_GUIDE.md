# Frontend Integration Guide

## Overview

Your FastAPI backend is now fully configured for React frontend integration with:
- ✅ CORS enabled for `http://localhost:3000` (and `http://localhost:5173` for Vite)
- ✅ Health check endpoint for availability verification
- ✅ Modern type-hinted Python code following PEP 8
- ✅ Production-ready API endpoints

---

## CORS Configuration

### What Was Added

CORS (Cross-Origin Resource Sharing) middleware is configured in [app/main.py](app/main.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # ["http://localhost:3000", "http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Configuration Details

| Setting | Value | Purpose |
|---------|-------|---------|
| `allow_origins` | `["http://localhost:3000", "http://localhost:5173"]` | Allow requests from React and Vite dev servers |
| `allow_credentials` | `True` | Allow authentication cookies if needed |
| `allow_methods` | `["*"]` | Allow all HTTP methods (GET, POST, PUT, DELETE, etc.) |
| `allow_headers` | `["*"]` | Allow all header types including Content-Type |

### Changing Origins

To add more origins (e.g., production URL), edit [app/config.py](app/config.py):

```python
cors_origins: list = [
    "http://localhost:3000",      # React dev
    "http://localhost:5173",      # Vite dev
    "https://yourdomain.com",     # Production
]
```

---

## Health Check Endpoint

### Purpose

Simple endpoint to verify server availability before making requests.

### Endpoint Details

**URL:** `GET /health`

**Response:** 
```json
{
  "status": "ok"
}
```

**Status Code:** 200 (always, when server is running)

### React Usage Example

```javascript
// Check if API server is running
const checkServerHealth = async () => {
  try {
    const response = await fetch("http://localhost:8000/health");
    const data = await response.json();
    console.log("Server status:", data.status); // Output: ok
    return data.status === "ok";
  } catch (error) {
    console.error("Server is not running:", error);
    return false;
  }
};

// Usage
if (await checkServerHealth()) {
  console.log("✅ Ready to make API requests");
} else {
  console.log("❌ Please start the API server");
}
```

---

## API Endpoint Reference

### Root Info Endpoint

**URL:** `GET /`

**Response:**
```json
{
  "message": "Welcome to AI Short Story Generator API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "model_loaded": true,
  "device": "cuda",
  "endpoints": {
    "health": "/health",
    "generate": "/api/v1/generate",
    "api_docs": "/docs"
  }
}
```

### Story Generation Endpoint

**URL:** `POST /api/v1/generate`

**Request Body:**
```json
{
  "name": "Minh",
  "personality": "dũng cảm",
  "setting": "một ngôi làng ven biển",
  "theme": "phiêu lưu"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "story": "Minh là một chàng trai dũng cảm sống ở một ngôi làng ven biển...",
  "message": "Story generated successfully"
}
```

**Error Response (400, 500, 503):**
```json
{
  "detail": "Invalid input: All fields must be non-empty strings"
}
```

---

## React Implementation Examples

### 1. Basic Setup with Environment Variables

Create a `.env.local` file in your React project:

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_V1=http://localhost:8000/api/v1
```

Create an API service module:

```javascript
// src/services/api.js

const API_URL = process.env.REACT_APP_API_URL;
const API_V1 = process.env.REACT_APP_API_V1;

export const apiService = {
  // Check server health
  async checkHealth() {
    try {
      const response = await fetch(`${API_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  },

  // Get API info
  async getInfo() {
    const response = await fetch(`${API_URL}/`);
    if (!response.ok) throw new Error("Failed to fetch API info");
    return response.json();
  },

  // Generate story
  async generateStory(storyRequest) {
    const response = await fetch(`${API_V1}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(storyRequest),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Story generation failed");
    }
    
    return response.json();
  },
};
```

### 2. React Component Example

```javascript
// src/components/StoryGenerator.jsx

import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";

export function StoryGenerator() {
  const [formData, setFormData] = useState({
    name: "",
    personality: "",
    setting: "",
    theme: "",
  });
  const [story, setStory] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [serverOk, setServerOk] = useState(false);

  // Check server availability on mount
  useEffect(() => {
    const checkServer = async () => {
      const isHealthy = await apiService.checkHealth();
      setServerOk(isHealthy);
      if (!isHealthy) {
        setError("⚠️ API server is not running. Please start it first.");
      }
    };
    checkServer();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!serverOk) {
      setError("Server is not available");
      return;
    }

    setLoading(true);
    setError("");
    setStory("");

    try {
      // Validate input
      if (!formData.name || !formData.personality || !formData.setting || !formData.theme) {
        throw new Error("All fields are required");
      }

      // Call API
      const response = await apiService.generateStory(formData);
      
      if (response.status === "success") {
        setStory(response.story);
      } else {
        throw new Error(response.message || "Failed to generate story");
      }
    } catch (err) {
      setError(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>📖 Vietnamese Story Generator</h1>

      {!serverOk && (
        <div style={{ 
          padding: "10px", 
          backgroundColor: "#fee", 
          color: "#c33", 
          borderRadius: "4px",
          marginBottom: "15px"
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px" }}>
          <label>Character Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g., Minh"
            maxLength="100"
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Personality:</label>
          <input
            type="text"
            name="personality"
            value={formData.personality}
            onChange={handleChange}
            placeholder="e.g., dũng cảm"
            maxLength="100"
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Setting:</label>
          <input
            type="text"
            name="setting"
            value={formData.setting}
            onChange={handleChange}
            placeholder="e.g., một ngôi làng ven biển"
            maxLength="100"
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Theme:</label>
          <input
            type="text"
            name="theme"
            value={formData.theme}
            onChange={handleChange}
            placeholder="e.g., phiêu lưu"
            maxLength="100"
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !serverOk}
          style={{
            padding: "10px 20px",
            backgroundColor: serverOk ? "#007bff" : "#999",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: serverOk ? "pointer" : "not-allowed",
          }}
        >
          {loading ? "Generating..." : "Generate Story"}
        </button>
      </form>

      {error && !error.startsWith("⚠️") && (
        <div style={{ 
          padding: "10px", 
          backgroundColor: "#fee", 
          color: "#c33", 
          borderRadius: "4px",
          marginTop: "15px"
        }}>
          {error}
        </div>
      )}

      {story && (
        <div style={{
          marginTop: "20px",
          padding: "15px",
          backgroundColor: "#f0f8ff",
          borderRadius: "4px",
          border: "1px solid #ddd"
        }}>
          <h2>Generated Story:</h2>
          <p>{story}</p>
        </div>
      )}
    </div>
  );
}
```

### 3. Using with Fetch API (Fetch with Retry)

```javascript
// src/services/apiWithRetry.js

async function fetchWithRetry(url, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }
      return response;
    } catch (err) {
      if (i === retries - 1) throw err;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1))); // Backoff
    }
  }
}

export const apiService = {
  async generateStory(request) {
    const response = await fetchWithRetry(
      "http://localhost:8000/api/v1/generate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      }
    );
    return response.json();
  }
};
```

### 4. Using with Axios

```javascript
// src/services/apiWithAxios.js

import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 30000,
});

export const apiService = {
  async checkHealth() {
    try {
      await apiClient.get("/health");
      return true;
    } catch {
      return false;
    }
  },

  async generateStory(storyRequest) {
    const response = await apiClient.post("/api/v1/generate", storyRequest);
    return response.data;
  },
};
```

---

## Error Handling

### Common Errors

| Error | Status | Cause | Solution |
|-------|--------|-------|----------|
| Network error | - | Server not running | Start server: `uvicorn app.main:app --reload` |
| CORS error | - | Origin not allowed | Check CORS config in [app/config.py](app/config.py) |
| 400 Bad Request | 400 | Invalid input | Check field values (empty or too long) |
| 422 Unprocessable | 422 | Missing field | Provide all 4 required fields |
| 503 Service | 503 | Model not loaded | Check startup logs for model errors |
| 500 Internal | 500 | Generation error | Check server logs for details |

### Error Handling Pattern

```javascript
try {
  const response = await apiService.generateStory(formData);
  if (response.status === "success") {
    // Handle success
  }
} catch (error) {
  if (error.response?.status === 400) {
    setError("Please fill all fields correctly");
  } else if (error.response?.status === 503) {
    setError("Server is starting. Please try again in a moment.");
  } else if (error.response?.status === 500) {
    setError("Generation failed. Check server logs.");
  } else {
    setError("Network error. Is the server running?");
  }
}
```

---

## Development Setup

### 1. Start Backend Server

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### 2. Start React Frontend

```bash
# Create React App
npm start
# Server runs at: http://localhost:3000

# Or with Vite
npm run dev
# Server runs at: http://localhost:5173
```

### 3. Test Integration

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/

# Generate story
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"A","personality":"B","setting":"C","theme":"D"}'
```

---

## Production Deployment

### Update CORS Origins

Before deployment, update [app/config.py](app/config.py):

```python
cors_origins: list = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

### Update Frontend Environment

Create `.env.production` in React project:

```bash
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_API_V1=https://api.yourdomain.com/api/v1
```

### Health Check in Production

```javascript
// Retry health check with exponential backoff
async function ensureServerReady(maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/health`);
      if (response.ok) return true;
    } catch {}
    
    // Exponential backoff: 1s, 2s, 4s, 8s
    await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
  }
  throw new Error("Server not available");
}
```

---

## Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Generate Vietnamese story
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lan",
    "personality": "thông minh và tử tế",
    "setting": "một thành phố hiện đại",
    "theme": "tình bạn"
  }'
```

### Automated Testing

```javascript
// src/tests/api.test.js

describe("API Integration", () => {
  test("health endpoint returns ok", async () => {
    const response = await fetch("http://localhost:8000/health");
    const data = await response.json();
    expect(data.status).toBe("ok");
  });

  test("generate endpoint accepts valid input", async () => {
    const response = await fetch("http://localhost:8000/api/v1/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: "Test",
        personality: "test",
        setting: "test",
        theme: "test",
      }),
    });
    expect(response.ok).toBe(true);
    const data = await response.json();
    expect(data.status).toBe("success");
  });
});
```

---

## Key Features for Frontend

✅ **CORS Enabled** - Direct requests from React  
✅ **Health Check** - Verify server availability  
✅ **Clean JSON API** - Easy to parse responses  
✅ **Comprehensive Errors** - Clear error messages  
✅ **Type Hints** - Better IDE support in Python  
✅ **PEP 8 Compliant** - Professional code quality  
✅ **Interactive Docs** - Auto-generated at `/docs`  

---

## Next Steps

1. **Copy this guide to your React project**
2. **Create API service module** using examples above
3. **Build React components** that call the endpoints
4. **Test with health check** before making requests
5. **Handle errors properly** with user feedback
6. **Deploy to production** with updated origins

Your backend is ready for frontend integration! 🚀
