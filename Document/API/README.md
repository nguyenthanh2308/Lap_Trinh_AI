# 📡 API Documentation - Tài Liệu API

**Folder này chứa tất cả tài liệu liên quan đến API endpoints**

---

## 📚 Các File trong Folder Này

### 1. 📖 **API_ENDPOINT_GUIDE.md**
**Nội dung:**
- Tất cả endpoints khả dụng
- GET / - API info
- GET /health - Health check
- POST /api/v1/generate - Generate story
- Request/Response examples
- Error handling guide
- Curl examples
- Status codes (200, 400, 503, 500)

**Dành cho:** Ai muốn biết endpoints nào có sẵn

---

### 2. 📖 **ENDPOINT_IMPLEMENTATION.md**
**Nội dung:**
- Chi tiết triển khai POST /generate
- Parameter giải thích
- Generation parameters:
  - max_new_tokens=150
  - temperature=0.8
  - top_p=0.9
  - do_sample=True
- Performance tips
- Troubleshooting guide
- Common issues & solutions

**Dành cho:** Developer muốn hiểu chi tiết cách hoạt động

---

### 3. 📖 **ENDPOINT_COMPLETE.md**
**Nội dung:**
- Xác nhận endpoint hoàn thành
- Danh sách requirements đã làm
- Process flow diagram
- Logging output examples
- Quick test instructions
- Summary checklist

**Dành cho:** Xác minh endpoint đã xong, testing nhanh

---

### 4. 📖 **INPUT_SCHEMA_GUIDE.md**
**Nội dung:**
- StoryRequest schema
- Field definitions:
  - name (string, 1-100 chars)
  - personality (string, 1-100 chars)
  - setting (string, 1-100 chars)
  - theme (string, 1-100 chars)
- Validation rules
- Response schemas
- Error schemas

**Dành cho:** Frontend developer cần biết input format

---

## 🎯 Đọc Theo Thứ Tự

1. **Bắt đầu:** API_ENDPOINT_GUIDE.md (khái quát)
2. **Chi tiết:** ENDPOINT_IMPLEMENTATION.md (cách hoạt động)
3. **Schema:** INPUT_SCHEMA_GUIDE.md (dữ liệu)
4. **Kiểm thử:** ENDPOINT_COMPLETE.md (test examples)

---

## 🚀 Quick Links

- 📂 **Parent:** [`Document/`](../)
- 📂 **Frontend:** [`Document/Frontend/`](../Frontend/)
- 📂 **Setup:** [`Document/Setup/`](../Setup/)
- 📄 **Index:** [`Document/README.md`](../README.md)

---

## ✨ Summary

Folder này chứa **tất cả thông tin về API**:
- ✅ Endpoints nào
- ✅ Cách gửi request
- ✅ Format dữ liệu
- ✅ Response như thế nào
- ✅ Các lỗi có thể gặp

**Mục đích:** Giúp Frontend developer integrate dễ dàng
