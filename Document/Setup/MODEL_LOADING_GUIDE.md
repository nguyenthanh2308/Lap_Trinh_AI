# Model Loading & GPU Setup Guide

## Overview

The FastAPI backend now includes comprehensive model loading logic that:
- ✅ Loads fine-tuned models from a local folder
- ✅ Auto-detects GPU (CUDA) availability
- ✅ Falls back to CPU if GPU not available
- ✅ Stores model/tokenizer in `app.state` for easy access
- ✅ Handles missing model folder gracefully
- ✅ Proper startup/shutdown lifecycle management

## File Structure

```
backend/
├── app/
│   ├── config.py                    # Configuration with model_folder setting
│   ├── main.py                      # FastAPI app with lifespan manager
│   ├── models/
│   │   ├── model_loader.py          # ModelLoader with GPU detection
│   │   └── schema.py                # Pydantic schemas
│   └── api/routes/
│       └── story.py                 # Routes that access app.state.model
├── fine_tuned_model/                # Your fine-tuned model folder
│   ├── config.json
│   ├── pytorch_model.bin            # or model.safetensors
│   ├── tokenizer.json
│   ├── special_tokens_map.json
│   └── ...
└── requirements.txt
```

## Model Folder Structure

Your `./fine_tuned_model` folder must contain:

```
fine_tuned_model/
├── config.json                      # Model configuration (required)
├── pytorch_model.bin                # Model weights (required)
  OR
├── model.safetensors                # Alternative format
├── tokenizer.json                   # Tokenizer vocabulary (recommended)
├── special_tokens_map.json          # Special tokens mapping (optional)
└── ...other tokenizer files
```

## Configuration

### Setting Model Folder Path

Edit `.env` file or `config.py`:

```python
# Default path (relative)
MODEL_FOLDER=./fine_tuned_model

# Or absolute path
MODEL_FOLDER=/path/to/your/fine_tuned_model

# GPU settings (auto-detect if not set)
DEVICE=                             # Leave empty for auto-detect
DEVICE=cuda                         # Force GPU
DEVICE=cpu                          # Force CPU
```

### Auto-Detection Logic

The system automatically:

1. **Detects GPU Availability**
   ```python
   if torch.cuda.is_available():
       device = "cuda"
   else:
       device = "cpu"
   ```

2. **Selects Appropriate Data Type**
   - GPU (CUDA): `torch.float16` (faster, less memory)
   - CPU: `torch.float32` (more precise)

3. **Validates Model Folder**
   - Checks if folder exists
   - Verifies `config.json` exists
   - Checks for model weights (`pytorch_model.bin` or `model.safetensors`)

## Startup Process

When the server starts:

```
🚀 Application starting up...
Loading fine-tuned model from: ./fine_tuned_model
Loading tokenizer...
Loading model...
✅ Model loaded successfully on device: cuda
✅ Application is ready to accept requests!
```

### What Happens:

1. **Lifespan Context Manager** (`@asynccontextmanager`)
   - Runs on startup before accepting requests
   - Loads model and tokenizer
   - Stores in `app.state`

2. **Model Validation**
   - Checks model folder exists
   - Verifies required files present
   - Graceful error handling

3. **GPU Detection**
   - Detects CUDA availability
   - Logs GPU device name and CUDA version
   - Falls back to CPU if unavailable

4. **Model Loading**
   - Uses `AutoTokenizer.from_pretrained()`
   - Uses `AutoModelForCausalLM.from_pretrained()`
   - Sets pad token if not configured
   - Moves model to detected device
   - Sets model to evaluation mode

## Accessing Model in Routes

Routes can access the loaded model via `app.state`:

```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/generate")
async def generate_story(request: Request):
    # Access from app.state
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    device = request.app.state.device
    
    # Use for inference
    story = ModelLoader.generate_story(
        tokenizer=tokenizer,
        model=model,
        prompt=prompt,
        max_length=200,
        device=device
    )
    return story
```

## GPU Setup (Optional)

### If You Have NVIDIA GPU:

1. **Install CUDA Toolkit** (if not already installed)
   - Visit: https://developer.nvidia.com/cuda-downloads

2. **Update PyTorch with CUDA Support**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Verify GPU Access**
   ```python
   import torch
   print(torch.cuda.is_available())        # Should print: True
   print(torch.cuda.get_device_name(0))   # Should print GPU name
   ```

4. **Monitor GPU Usage**
   - Windows: `nvidia-smi` (requires NVIDIA drivers)
   - Python: 
   ```python
   import torch
   torch.cuda.memory_allocated()
   torch.cuda.memory_reserved()
   ```

## Error Handling

### Model Folder Not Found

```
❌ Failed to load model during startup: Invalid model folder: ./fine_tuned_model
Application will start but inference will fail.
```

**Fix:** 
- Create `./fine_tuned_model` folder in backend directory
- Copy your model files there
- Verify `config.json` and model weights exist

### Missing Model Files

```
ERROR: Model file (pytorch_model.bin or model.safetensors) not found in ./fine_tuned_model
```

**Fix:**
- Ensure model weights are in the folder
- Supported formats: `pytorch_model.bin`, `model.safetensors`
- File should be directly in model folder (not in subdirectory)

### CUDA Out of Memory

```
RuntimeError: CUDA out of memory
```

**Fixes:**
1. Use CPU: Set `DEVICE=cpu`
2. Reduce batch size
3. Use `torch.cuda.empty_cache()` (app does this on shutdown)
4. Use 8-bit quantization: `load_in_8bit=True`

## Shutdown Process

When server shuts down:

```
🛑 Application shutting down...
Cleaning up resources...
GPU memory cleaned up
✅ Shutdown complete
```

The app automatically:
- Cleans GPU memory cache
- Releases resources
- Logs shutdown events

## Testing Model Loading

### Test 1: Check Model is Loaded

```bash
curl http://localhost:8000/
```

Response should include:
```json
{
  "model_loaded": true,
  "device": "cuda"  // or "cpu"
}
```

### Test 2: Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda"
}
```

### Test 3: Generate Story

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Minh",
    "personality": "dũng cảm",
    "setting": "một ngôi làng ven biển",
    "theme": "phiêu lưu"
  }'
```

## Code Architecture

### ModelLoader Class

```python
class ModelLoader:
    @staticmethod
    def detect_device() -> str:
        """Auto-detect GPU or CPU"""
    
    @staticmethod
    def validate_model_folder(model_folder: str) -> bool:
        """Check if model folder is valid"""
    
    @staticmethod
    def load_model(model_folder: str, device: str = None):
        """Load tokenizer and model"""
        return tokenizer, model, device
    
    @staticmethod
    def generate_story(tokenizer, model, prompt, max_length, device):
        """Generate story from prompt"""
        return story
```

### Lifespan Context Manager

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    tokenizer, model, device = ModelLoader.load_model(...)
    app.state.tokenizer = tokenizer
    app.state.model = model
    app.state.device = device
    
    yield  # App runs here
    
    # SHUTDOWN
    torch.cuda.empty_cache()
```

## Performance Tips

1. **Use GPU for Better Performance**
   - GPU inference is 10-100x faster than CPU
   - Requires NVIDIA GPU and CUDA installed

2. **Optimize Model Loading**
   - Model loads once at startup (not per request)
   - Stored in app.state (fast access)

3. **Batch Requests (Future Enhancement)**
   - Can queue multiple inference requests
   - Process in parallel for better throughput

4. **Use Quantization**
   - 8-bit or 4-bit quantization reduces memory
   - Slightly lower quality but much faster

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not loading | Check model folder path, verify files exist |
| GPU not detected | Reinstall PyTorch with CUDA support |
| Out of memory | Use CPU or reduce max_length |
| Slow inference | Use GPU, reduce model size, or use quantization |
| 503 error on /generate | Check server logs, model may not have loaded |

## Next Steps

1. ✅ Place your fine-tuned model in `./fine_tuned_model`
2. ✅ Run server: `uvicorn app.main:app --reload`
3. ✅ Test endpoints at `http://localhost:8000/docs`
4. ✅ Monitor logs for load status
5. ✅ Adjust configuration if needed

## References

- [Transformers Library Documentation](https://huggingface.co/docs/transformers)
- [PyTorch CUDA Setup](https://pytorch.org/get-started/locally/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
