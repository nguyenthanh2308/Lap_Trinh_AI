# Input Schema & Prompt Construction

## StoryRequest Pydantic Model

**File:** `app/models/schema.py`

```python
from pydantic import BaseModel, Field

class StoryRequest(BaseModel):
    """Request body for story generation"""
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    personality: str = Field(..., min_length=1, max_length=100, description="Character personality")
    setting: str = Field(..., min_length=1, max_length=100, description="Story setting")
    theme: str = Field(..., min_length=1, max_length=100, description="Story theme")
```

### Field Specifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `name` | str | 1-100 chars | Character name (required) |
| `personality` | str | 1-100 chars | Character personality traits (required) |
| `setting` | str | 1-100 chars | Story setting/location (required) |
| `theme` | str | 1-100 chars | Story theme/genre (required) |

### Validation

- All fields are required (`...` means no default)
- Minimum length: 1 character (no empty strings)
- Maximum length: 100 characters each
- All values must be strings

---

## build_prompt() Function

**File:** `app/utils/helpers.py`

```python
def build_prompt(request: StoryRequest) -> str:
    """
    Build a formatted Vietnamese prompt from StoryRequest model.
    
    Args:
        request: StoryRequest containing name, personality, setting, theme
        
    Returns:
        Formatted prompt string in Vietnamese
    """
    prompt = (
        f"Nhân vật: {request.name} | "
        f"Tính cách: {request.personality} | "
        f"Bối cảnh: {request.setting} | "
        f"Chủ đề: {request.theme}. Truyện: "
    )
    return prompt
```

### Prompt Format

**Template:**
```
Nhân vật: {name} | Tính cách: {personality} | Bối cảnh: {setting} | Chủ đề: {theme}. Truyện: 
```

**Example Input:**
```json
{
  "name": "Minh",
  "personality": "dũng cảm",
  "setting": "một ngôi làng ven biển",
  "theme": "phiêu lưu"
}
```

**Example Output:**
```
Nhân vật: Minh | Tính cách: dũng cảm | Bối cảnh: một ngôi làng ven biển | Chủ đề: phiêu lưu. Truyện: 
```

### Key Features

- ✅ Takes StoryRequest object directly (type-safe)
- ✅ Returns properly formatted Vietnamese string
- ✅ Exact format: Vietnamese labels with pipe separators
- ✅ Ends with "Truyện: " (story prompt)
- ✅ Standalone utility function

---

## Usage in Routes

**File:** `app/api/routes/story.py`

```python
from app.utils.helpers import build_prompt

@router.post("/generate")
async def generate_story(request: StoryRequest, http_request: Request) -> StoryResponse:
    # Build prompt from request
    prompt = build_prompt(request)
    logger.info(f"Generated prompt: {prompt}")
    
    # Pass to model for story generation
    story = ModelLoader.generate_story(
        tokenizer=app_state.tokenizer,
        model=app_state.model,
        prompt=prompt,
        max_length=settings.max_length,
        device=app_state.device
    )
    
    # Return only generated part (remove prompt)
    generated_part = story.replace(prompt, "", 1).strip()
    return StoryResponse(status="success", story=generated_part)
```

---

## API Request Example

### Using curl

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

### Using Python requests

```python
import requests

payload = {
    "name": "Minh",
    "personality": "dũng cảm",
    "setting": "một ngôi làng ven biển",
    "theme": "phiêu lưu"
}

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json=payload
)

print(response.json())
```

### Using FastAPI TestClient

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.post(
    "/api/v1/generate",
    json={
        "name": "Minh",
        "personality": "dũng cảm",
        "setting": "một ngôi làng ven biển",
        "theme": "phiêu lưu"
    }
)

assert response.status_code == 200
assert response.json()["status"] == "success"
```

---

## API Response Example

### Success Response

```json
{
  "status": "success",
  "story": "Minh là một chàng trai dũng cảm sống ở một ngôi làng ven biển. Anh yêu thích phiêu lưu và khám phá...",
  "message": "Story generated successfully"
}
```

### Validation Error Response

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 character",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Service Unavailable (Model Not Loaded)

```json
{
  "detail": "Model is not loaded. Please check server logs."
}
```

---

## Input Validation

### Valid Inputs ✅

```json
{
  "name": "Lan",
  "personality": "thông minh",
  "setting": "thành phố",
  "theme": "tình yêu"
}
```

```json
{
  "name": "A",
  "personality": "B",
  "setting": "C",
  "theme": "D"
}
```

### Invalid Inputs ❌

```json
{
  "name": "",
  "personality": "dũng cảm",
  "setting": "làng",
  "theme": "phiêu lưu"
}
```
Error: `name` minimum length is 1

```json
{
  "name": "Minh",
  "personality": "dũng cảm",
  "setting": "làng"
}
```
Error: `theme` is required

---

## Testing

### Test with curl

```bash
# Valid request
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"Minh","personality":"dũng cảm","setting":"làng","theme":"phiêu lưu"}'

# Invalid - empty name
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"","personality":"dũng cảm","setting":"làng","theme":"phiêu lưu"}'

# Invalid - missing field
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"Minh","personality":"dũng cảm"}'
```

### Test via Swagger UI

1. Open: `http://localhost:8000/docs`
2. Find `POST /api/v1/generate`
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "name": "Minh",
     "personality": "dũng cảm",
     "setting": "một ngôi làng ven biển",
     "theme": "phiêu lưu"
   }
   ```
5. Click "Execute"
6. View the response

---

## Summary

| Component | Details |
|-----------|---------|
| **Model** | `StoryRequest` with 4 required fields |
| **Function** | `build_prompt(request: StoryRequest) -> str` |
| **Format** | Vietnamese with exact structure |
| **Location** | `app/utils/helpers.py` |
| **Usage** | `app/api/routes/story.py` |
| **Type Safety** | ✅ Pydantic validation |
| **Testing** | Can test via API docs or curl |
