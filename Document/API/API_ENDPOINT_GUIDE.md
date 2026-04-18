# POST /generate Endpoint Documentation

## Overview

The `POST /api/v1/generate` endpoint generates a Vietnamese short story based on character details provided in the request.

**Endpoint:** `POST /api/v1/generate`  
**Base URL:** `http://localhost:8000/api/v1`  
**Content-Type:** `application/json`

---

## Request

### Request Body (StoryRequest)

```json
{
  "name": "string (1-100 chars)",
  "personality": "string (1-100 chars)",
  "setting": "string (1-100 chars)",
  "theme": "string (1-100 chars)"
}
```

### Field Descriptions

| Field | Type | Required | Length | Description |
|-------|------|----------|--------|-------------|
| `name` | string | Yes | 1-100 | Character/protagonist name |
| `personality` | string | Yes | 1-100 | Character personality traits or characteristics |
| `setting` | string | Yes | 1-100 | Story location or environment |
| `theme` | string | Yes | 1-100 | Story theme or genre |

### Example Request

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

### Example Request (Python)

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

---

## Response

### Success Response (200 OK)

**Status Code:** `200`

**Response Body:**
```json
{
  "status": "success",
  "story": "Minh là một chàng trai dũng cảm sống ở một ngôi làng ven biển...",
  "message": "Story generated successfully"
}
```

### Error Responses

#### 400 Bad Request - Invalid Input

When any field is empty or invalid:

```json
{
  "detail": "Invalid input: All fields must be non-empty strings"
}
```

**Causes:**
- Empty string in any field
- Field missing from request
- Field value exceeds 100 characters

---

#### 503 Service Unavailable - Model Not Loaded

When the AI model failed to load:

```json
{
  "detail": "Model is not loaded. Please check server logs."
}
```

**Causes:**
- Model folder not found at startup
- Model files missing or corrupted
- CUDA/GPU issues during loading

**Solution:** Check server startup logs for model loading errors

---

#### 500 Internal Server Error - Generation Failed

When the story generation process fails:

```json
{
  "detail": {
    "error": "CUDA out of memory",
    "status": "error"
  }
}
```

**Common Causes:**
- CUDA out of memory (GPU too small)
- Invalid model weights
- Encoding/decoding error
- Tokenizer issue

**Solutions:**
- Use CPU: Set `DEVICE=cpu` in `.env`
- Reduce `MAX_LENGTH` in `.env`
- Restart server to clear memory

---

## Generation Parameters

The endpoint uses these parameters for story generation:

```python
model.generate(
    input_ids,
    max_new_tokens=150,      # Max 150 new tokens after prompt
    temperature=0.8,         # Creativity level (0.7-0.9 range)
    top_p=0.9,              # Nucleus sampling (diverse but sensible)
    do_sample=True,         # Enable sampling for variation
    pad_token_id=...,       # Padding token
    eos_token_id=...,       # End-of-sequence token
    num_return_sequences=1  # Generate 1 story per request
)
```

### Parameter Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `max_new_tokens` | 150 | Prevents stories that are too long |
| `temperature` | 0.8 | Balances creativity (higher = more creative) |
| `top_p` | 0.9 | Nucleus sampling for quality diversity |
| `do_sample` | True | Enables random sampling instead of greedy decoding |
| `num_return_sequences` | 1 | Generates one story per request |

---

## Processing Flow

```
1. Client sends StoryRequest
   ↓
2. Endpoint validates input (all fields non-empty)
   ↓
3. build_prompt() creates Vietnamese string:
   "Nhân vật: Minh | Tính cách: dũng cảm | Bối cảnh: ... | Chủ đề: ... . Truyện: "
   ↓
4. Prompt is encoded to token IDs
   ↓
5. Model generates with parameters:
   - max_new_tokens=150
   - temperature=0.8
   - top_p=0.9
   - do_sample=True
   ↓
6. Output tokens are decoded to UTF-8 Vietnamese text
   ↓
7. Prompt is removed from generated text
   ↓
8. Story (only generated part) returned to client
```

---

## Example Complete Flow

### Request

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lan",
    "personality": "thông minh",
    "setting": "thành phố",
    "theme": "tình yêu"
  }'
```

### Internal Processing

1. **Validation:** ✅ All fields present and non-empty
2. **Prompt Building:**
   ```
   Nhân vật: Lan | Tính cách: thông minh | Bối cảnh: thành phố | Chủ đề: tình yêu. Truyện: 
   ```
3. **Encoding:** Converts prompt to token IDs
4. **Generation:** Model generates ~150 new tokens
5. **Decoding:** Converts tokens back to Vietnamese text
6. **Processing:** Removes prompt, keeps only story

### Response

```json
{
  "status": "success",
  "story": "Lan là một cô gái thông minh sống ở thành phố lớn. Cô có một trái tim tốt đẹp và luôn sẵn sàng giúp đỡ người khác. Một ngày, cô gặp một chàng trai và...",
  "message": "Story generated successfully"
}
```

---

## Error Handling

### Try-Except Structure

```python
try:
    # 1. Get model from app.state
    # 2. Validate input
    # 3. Build prompt
    # 4. Encode input
    # 5. Generate with model
    # 6. Decode output
    # 7. Return success
except HTTPException:
    # Re-raise HTTP errors (400, 503)
    raise
except Exception as e:
    # Catch all other errors
    logger.error(f"Error: {str(e)}")
    # Return 500 with error details
    raise HTTPException(
        status_code=500,
        detail={"error": str(e), "status": "error"}
    )
```

### Logged Information

For debugging, the endpoint logs:

```
Generated prompt: Nhân vật: Minh | Tính cách: dũng cảm | ...
Input shape: torch.Size([1, 25])
Generating story with model...
Generated output shape: torch.Size([1, 172])
Generated story (145 chars): Minh là một chàng trai dũng cảm...
```

---

## Testing

### Using curl

```bash
# Success case
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"A","personality":"B","setting":"C","theme":"D"}'

# Invalid - empty field
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"","personality":"B","setting":"C","theme":"D"}'

# Invalid - missing field
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"A","personality":"B"}'
```

### Using Swagger UI

1. Open: `http://localhost:8000/docs`
2. Find section: `story`
3. Click: `POST /api/v1/generate`
4. Click: `Try it out`
5. Fill request body with JSON
6. Click: `Execute`
7. View response

### Using Python TestClient

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test success
response = client.post(
    "/api/v1/generate",
    json={
        "name": "Minh",
        "personality": "dũng cảm",
        "setting": "làng",
        "theme": "phiêu lưu"
    }
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert len(response.json()["story"]) > 0

# Test invalid input
response = client.post(
    "/api/v1/generate",
    json={"name": "", "personality": "B", "setting": "C", "theme": "D"}
)
assert response.status_code == 400
```

---

## Performance Considerations

### Generation Time

Expected generation time depends on:
- **Hardware:** GPU ~5-10s, CPU ~30-60s
- **Model size:** Larger models take longer
- **Token length:** 150 tokens takes ~1-2s on GPU

### Memory Usage

- **GPU (CUDA):** ~2-4 GB VRAM
- **CPU:** ~1-2 GB RAM
- **Reduced during shutdown:** CUDA cache cleared

### Optimization Tips

1. **Use GPU if available** - 10x faster than CPU
2. **Reuse model in app.state** - Loaded once, not per request
3. **Monitor token length** - Shorter = faster
4. **Check logs** - Logs show generation timing

---

## Integration Examples

### React Frontend

```javascript
async function generateStory(formData) {
  const response = await fetch('http://localhost:8000/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: formData.name,
      personality: formData.personality,
      setting: formData.setting,
      theme: formData.theme
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail?.error || 'Generation failed');
  }
  
  const data = await response.json();
  return data.story;
}
```

### Node.js Backend

```javascript
const axios = require('axios');

async function generateStory(details) {
  try {
    const response = await axios.post(
      'http://localhost:8000/api/v1/generate',
      {
        name: details.name,
        personality: details.personality,
        setting: details.setting,
        theme: details.theme
      }
    );
    return response.data.story;
  } catch (error) {
    console.error('Generation error:', error.response.data);
    throw error;
  }
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **503 Model not loaded** | Model files missing | Check server startup logs |
| **400 Invalid input** | Empty field or missing field | Verify all 4 fields are non-empty |
| **500 CUDA out of memory** | GPU too small for model | Set `DEVICE=cpu` or reduce `MAX_LENGTH` |
| **500 Tokenizer error** | Bad model format | Verify model folder structure |
| **Slow response** | Using CPU | Verify GPU setup with `nvidia-smi` |
| **Empty story** | Model issue | Check model weights and config |

---

## Summary

| Aspect | Details |
|--------|---------|
| **Endpoint** | `POST /api/v1/generate` |
| **Input** | StoryRequest (4 string fields) |
| **Processing** | Prompt building → Encoding → Generation → Decoding |
| **Parameters** | max_new_tokens=150, temperature=0.8, top_p=0.9, do_sample=True |
| **Output** | JSON with story text and status |
| **Error Handling** | Try-except with detailed error responses |
| **Logging** | Detailed logs for debugging |
| **Testing** | curl, Swagger UI, Python TestClient |

Your story generation endpoint is production-ready! 🚀
