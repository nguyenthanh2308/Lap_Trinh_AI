# 💻 Frontend Integration - Tích hợp Frontend

**Folder này chứa hướng dẫn tích hợp React frontend với Backend**

---

## 📚 Các File trong Folder Này

### 1. 📖 **FRONTEND_INTEGRATION_GUIDE.md**
**Nội dung:**
- Hướng dẫn React integration hoàn chỉnh
- CORS configuration explanation
- Health check endpoint
- API service examples (Fetch & Axios)
- React component examples
- Error handling patterns
- Development setup
- Production deployment
- Testing examples

**Dành cho:** React developer muốn integrate với Backend

**Bao gồm:**
- Environment variables setup
- API service module
- React component với hooks
- Error handling
- Retry logic
- Health check implementation

---

### 2. 📖 **FRONTEND_READY.md**
**Nội dung:**
- Xác nhận CORS đã setup
- Health endpoint working
- Quick verification checklist
- Backend endpoints reference
- React code examples
- Next steps

**Dành cho:** Xác minh backend sẵn sàng cho frontend

---

## 🎯 Quy Trình Integrate - Integration Process

### Step 1: Chuẩn bị Backend
- ✅ CORS configured for localhost:3000
- ✅ Health endpoint available
- ✅ API endpoints ready

### Step 2: Chuẩn bị React
- ✅ Create environment variables (.env.local)
- ✅ Create API service module
- ✅ Build React components

### Step 3: Test Integration
- ✅ Test health endpoint
- ✅ Test story generation
- ✅ Check error handling

---

## 💡 Quick Start - Bắt Đầu Nhanh

### 1. Backend Running?
```bash
curl http://localhost:8000/health
# Response: {"status":"ok"}
```

### 2. React Code
```javascript
// API Service
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Minh',
    personality: 'dũng cảm',
    setting: 'làng ven biển',
    theme: 'phiêu lưu'
  })
});

const { story } = await response.json();
```

### 3. Environment Variables
```bash
# .env.local
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_V1=http://localhost:8000/api/v1
```

---

## 📂 Sử Dụng Theo Thứ Tự

1. **Kiểm tra:** FRONTEND_READY.md (verify backend ready)
2. **Hướng dẫn:** FRONTEND_INTEGRATION_GUIDE.md (detail setup)
3. **Code:** Copy examples từ guide
4. **Test:** Test endpoints

---

## 🔐 CORS Configuration

**Đã cấu hình cho:**
- ✅ http://localhost:3000 (React dev)
- ✅ http://localhost:5173 (Vite dev)

**Cho production, update:**
```python
# Document/Setup/MODEL_LOADING_GUIDE.md
cors_origins: list = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

## 🚀 Quick Links

- 📂 **Parent:** [`Document/`](../)
- 📂 **API:** [`Document/API/`](../API/)
- 📂 **Setup:** [`Document/Setup/`](../Setup/)
- 📄 **Index:** [`Document/README.md`](../README.md)

---

## ✨ Summary

Folder này giúp:
- ✅ Hiểu CORS là gì
- ✅ Setup API service
- ✅ Viết React components
- ✅ Handle errors
- ✅ Test integration

**Mục đích:** Frontend developer có thể integrate nhanh chóng
