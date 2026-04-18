# AI Short Story Generator - Backend

## Overview
This is the backend service for the AI-Powered Short Story Generator. It uses FastAPI, Transformers, and PyTorch to generate short stories based on user input parameters.

## Project Structure
```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── story.py          # Story generation endpoints
│   ├── models/
│   │   ├── schema.py             # Pydantic models for request/response
│   │   └── model_loader.py       # Model loading and inference logic
│   ├── utils/
│   │   └── helpers.py            # Utility functions
│   ├── config.py                 # Application configuration
│   └── main.py                   # FastAPI app creation
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Setup Instructions

### 1. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env file if needed (usually default settings work)
```

### 4. Run the Server

**Development Mode (with auto-reload):**
```bash
uvicorn app.main:app --reload
```

**Production Mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/api/v1/health`
  - Response: `{"status": "healthy", "app": "...", "version": "..."}`

### Generate Story
- **POST** `/api/v1/generate`
  - Request Body:
    ```json
    {
      "name": "Minh",
      "personality": "dũng cảm",
      "setting": "một ngôi làng ven biển",
      "theme": "phiêu lưu"
    }
    ```
  - Response:
    ```json
    {
      "status": "success",
      "story": "Generated story text...",
      "message": "Story generated successfully"
    }
    ```

### API Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Dependencies

### Core Framework
- **FastAPI** (0.104.1): Modern web framework for building APIs
- **Uvicorn** (0.24.0): ASGI web server

### AI/ML Libraries
- **Transformers** (4.36.0): Hugging Face models
- **PyTorch** (2.1.1): Deep learning framework
- **NumPy** (1.24.3): Numerical computing

### Data Validation
- **Pydantic** (2.5.0): Data validation using Python type annotations
- **Pydantic-settings** (2.1.0): Settings management

### Utilities
- **python-dotenv** (1.0.0): Load environment variables from .env
- **aiofiles** (23.2.1): Async file operations

## Configuration

Environment variables (in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | false | Enable debug mode |
| `MODEL_NAME` | gpt2 | Model name from Hugging Face |
| `DEVICE` | cpu | torch device (cpu or cuda) |
| `MAX_LENGTH` | 200 | Max length of generated story |
| `PORT` | 8000 | Server port |

## Development Notes

### Using GPU (if available)
Set `DEVICE=cuda` in `.env`:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Loading Custom Fine-tuned Models
Replace `MODEL_NAME` in `.env` with the path to your fine-tuned model:
```
MODEL_NAME=./models/my-fine-tuned-model
```

### Logging
The application logs to console. For file logging, modify `app/main.py`

## Common Issues

### torch not installed correctly
```bash
pip install torch --force-reinstall --no-cache-dir
```

### CORS Issues
Update `CORS_ORIGINS` in `app/config.py` with your frontend URL

### Model download issues
Set `HF_HOME` environment variable:
```bash
$env:HF_HOME = "D:\cache\huggingface"
```

## License
MIT
