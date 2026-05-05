# Quick Reference Guide - Model Loading

## 🚀 Quick Start

### 1. Prepare Model Folder
```
backend/
└── fine_tuned_model/
    ├── config.json              (required)
    ├── pytorch_model.bin        (or model.safetensors)
    ├── tokenizer.json
    └── special_tokens_map.json
```

### 2. Install Dependencies
```bash
cd backend
python -m venv venv
http://localhost:20128
pip install -r requirements.txt
```

### 3. Run Server
```bash
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### 4. Test
Visit: `http://localhost:8000/docs`

---

## 🔑 Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Auto GPU Detection** | Detects CUDA and falls back to CPU | ✅ |
| **Local Model Loading** | Loads from `./fine_tuned_model` folder | ✅ |
| **Model Validation** | Checks required files exist | ✅ |
| **App State Storage** | Model stored in `request.app.state` | ✅ |
| **Startup Logging** | Shows device and model status | ✅ |
| **Error Handling** | Graceful errors with detailed messages | ✅ |
| **GPU Cleanup** | Clears CUDA memory on shutdown | ✅ |

---

## 📝 Configuration

```env
# .env file
MODEL_FOLDER=./fine_tuned_model    # Path to your model
DEVICE=                             # Leave empty to auto-detect
                                    # Set to "cuda" for GPU
                                    # Set to "cpu" for CPU
MAX_LENGTH=200                      # Max generation length
```

---

## 📊 Logs Output

### Successful Startup
```
2026-04-18 10:30:45 - __main__ - INFO - 🚀 Application starting up...
2026-04-18 10:30:45 - __main__ - INFO - Loading fine-tuned model from: ./fine_tuned_model
2026-04-18 10:30:45 - app.models.model_loader - INFO - Model folder validation passed
2026-04-18 10:30:45 - app.models.model_loader - INFO - GPU detected: NVIDIA GeForce RTX 3080
2026-04-18 10:30:45 - app.models.model_loader - INFO - CUDA version: 11.8
2026-04-18 10:30:45 - app.models.model_loader - INFO - Loading tokenizer...
2026-04-18 10:30:46 - app.models.model_loader - INFO - Loading model...
2026-04-18 10:30:48 - app.models.model_loader - INFO - ✅ Model and tokenizer loaded successfully!
2026-04-18 10:30:48 - __main__ - INFO - ✅ Model loaded successfully on device: cuda
2026-04-18 10:30:48 - __main__ - INFO - ✅ Application is ready to accept requests!
```

### CPU Fallback
```
2026-04-18 10:30:45 - app.models.model_loader - INFO - No GPU detected, using CPU
2026-04-18 10:30:48 - app.models.model_loader - INFO - ✅ Model and tokenizer loaded successfully!
2026-04-18 10:30:48 - __main__ - INFO - ✅ Model loaded successfully on device: cpu
```

### Error Case
```
2026-04-18 10:30:45 - app.models.model_loader - ERROR - Model folder not found: ./fine_tuned_model
2026-04-18 10:30:45 - __main__ - ERROR - ❌ Failed to load model during startup
2026-04-18 10:30:45 - __main__ - INFO - Application will start but inference will fail.
```

---

## 🔌 API Endpoints

### Root Endpoint
```bash
GET http://localhost:8000/
```
Response:
```json
{
  "message": "Welcome to AI Short Story Generator API",
  "version": "1.0.0",
  "docs": "/docs",
  "model_loaded": true
}
```

### Health Check
```bash
GET http://localhost:8000/api/v1/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda"
}
```

### Generate Story
```bash
POST http://localhost:8000/api/v1/generate
Content-Type: application/json

{
  "name": "Minh",
  "personality": "dũng cảm",
  "setting": "một ngôi làng ven biển",
  "theme": "phiêu lưu"
}
```
Response:
```json
{
  "status": "success",
  "story": "Nhân vật Minh là một chàng trai dũng cảm...",
  "message": "Story generated successfully"
}
```

### Error Response (503 - Model Not Loaded)
```json
{
  "detail": "Model is not loaded. Please check server logs."
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Model folder not found** | Check folder path in config.py or .env |
| **config.json missing** | Verify all model files are in folder |
| **GPU not detected** | Reinstall PyTorch with CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu118` |
| **CUDA out of memory** | Set `DEVICE=cpu` or reduce `MAX_LENGTH` |
| **Slow inference** | Make sure using GPU (`device: "cuda"`) |
| **503 on /generate** | Check server logs for model load errors |

---

## 📚 Full Documentation

- **MODEL_LOADING_GUIDE.md** - Complete setup guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **README.md** - Project overview

---

## 💡 Common Tasks

### Check if GPU is Available
```python
import torch
print(torch.cuda.is_available())        # True or False
print(torch.cuda.get_device_name(0))   # GPU name
```

### Force CPU in .env
```env
DEVICE=cpu
```

### Monitor GPU Usage (Windows)
```bash
nvidia-smi
```

### Clear GPU Memory Manually
```python
import torch
torch.cuda.empty_cache()
```

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
├─────────────────────────────────────────┤
│  Lifespan Manager                       │
│  ├─ Startup: Load model + tokenizer     │
│  ├─ Store in app.state                  │
│  └─ Shutdown: Cleanup GPU               │
├─────────────────────────────────────────┤
│  API Routes                             │
│  ├─ GET  /  (root)                      │
│  ├─ GET  /api/v1/health                 │
│  └─ POST /api/v1/generate               │
├─────────────────────────────────────────┤
│  ModelLoader (static methods)           │
│  ├─ detect_device()                     │
│  ├─ validate_model_folder()             │
│  ├─ load_model()                        │
│  └─ generate_story()                    │
├─────────────────────────────────────────┤
│  Resources                              │
│  ├─ fine_tuned_model/ (local)           │
│  ├─ GPU (if available)                  │
│  └─ CPU (fallback)                      │
└─────────────────────────────────────────┘
```

---

## ✅ Checklist

- [ ] Place model in `./fine_tuned_model` folder
- [ ] Verify `config.json` and model weights exist
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `.\venv\Scripts\Activate.ps1`
- [ ] Install deps: `pip install -r requirements.txt`
- [ ] Run server: `uvicorn app.main:app --reload`
- [ ] Test at: `http://localhost:8000/docs`
- [ ] Check logs for GPU detection
- [ ] Generate a test story

---

## 📞 Support

For issues or questions:
1. Check logs in console output
2. Visit API docs: `http://localhost:8000/docs`
3. See **MODEL_LOADING_GUIDE.md** for detailed troubleshooting
4. Review **IMPLEMENTATION_SUMMARY.md** for technical details
