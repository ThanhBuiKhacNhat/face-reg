# Dataset Folder - Hướng dẫn để có Face Recognition chất lượng cao

## 📁 Cách tổ chức ảnh theo folder (KHUYẾN NGHỊ)

### ✅ Cấu trúc folder mới - dễ quản lý:
```
dataset/
├── thanh/              📁 Folder riêng cho Thanh
│   ├── main.jpg        (ảnh chính - mặt thẳng)
│   ├── side.jpg        (góc nghiêng)
│   ├── smile.jpg       (cười tươi)
│   └── glasses.jpg     (đeo kính)
├── john_doe/           📁 Folder riêng cho John Doe  
│   ├── portrait.jpg    (chân dung)
│   ├── casual.jpg      (thường ngày)
│   └── office.jpg      (công sở)
├── jane_smith/         📁 Folder riêng cho Jane Smith
│   ├── photo1.jpg      
│   ├── photo2.jpg      
│   ├── photo3.jpg      
│   └── photo4.jpg      
└── README.md
```

### 💡 Hướng dẫn tạo folder mới:
1. **Tạo folder** với tên người (dùng `_` thay khoảng trắng)
2. **Thêm 3-5 ảnh** chất lượng cao vào folder  
3. **Click "Reload Faces"** trong app để train lại
4. **Kiểm tra kết quả** - xem training summary

### 🔄 Cấu trúc cũ vẫn được hỗ trợ:
```
dataset/
├── thanh.jpg          (ảnh chính)
├── thanh_1.jpg        (ảnh bổ sung #1) 
├── thanh_2.jpg        (ảnh bổ sung #2)
└── john_doe.jpg
```

## 🎯 Ưu điểm của cấu trúc folder:

✅ **Tổ chức tốt hơn**: Mỗi người có folder riêng  
✅ **Dễ quản lý**: Thêm/xóa ảnh dễ dàng  
✅ **Linh hoạt**: Tên file không cần theo quy tắc nghiêm ngặt  
✅ **Mở rộng**: Có thể thêm nhiều ảnh bất kì  
✅ **Rõ ràng**: Biết ngay ảnh nào của ai  

## ⭐ Chất lượng nhận diện theo số lượng ảnh:

- **1 ảnh** = ⭐ (Cơ bản) - Có thể nhận diện nhưng không ổn định
- **2 ảnh** = ⭐⭐ (Tốt) - Nhận diện khá chính xác  
- **3+ ảnh** = ⭐⭐⭐ (Xuất sắc) - Nhận diện rất chính xác và ổn định

## 📋 Yêu cầu về ảnh:

### Format hỗ trợ:
- JPG, JPEG, PNG

### Chất lượng ảnh:
- **Độ phân giải**: Tối thiểu 200x200 pixels
- **Ánh sáng**: Đầy đủ, tránh quá tối hoặc quá sáng
- **Góc chụp**: Chủ yếu là mặt thẳng, có thể thêm góc nghiêng nhẹ
- **Khuôn mặt**: Rõ ràng, không bị che khuất

### Đa dạng ảnh cho mỗi người:
1. **Ảnh chính** (`main.jpg`): Mặt thẳng, ánh sáng tốt
2. **Ảnh góc nghiêng** (`side.jpg`): Hơi nghiêng trái/phải  
3. **Ảnh biểu cảm khác** (`smile.jpg`): Cười, nghiêm túc
4. **Ảnh điều kiện khác** (`glasses.jpg`): Đeo kính, không đeo kính

## 🚫 Tránh các loại ảnh sau:

- Đeo khẩu trang che khuất mặt
- Đeo kính râm đậm  
- Ánh sáng quá tối hoặc ngược sáng
- Khuôn mặt quá nhỏ trong ảnh
- Nhiều người trong cùng 1 ảnh
- Ảnh mờ, bị nhòe

## 🎯 Tips để có kết quả tốt nhất:

1. **Chụp ở nhiều thời điểm khác nhau** - sáng, chiều, tối
2. **Thay đổi trang phục** - có kính, không kính, mũ, không mũ
3. **Biểu cảm đa dạng** - cười, nghiêm túc, ngạc nhiên
4. **Góc độ khác nhau** - thẳng, nghiêng nhẹ 15-30 độ  
5. **Khoảng cách khác nhau** - gần (vai trở lên), xa (nửa người)

## 🔧 Điều chỉnh độ nhạy:

Nếu hệ thống nhận diện sai:
- **Quá nghiêm ngặt** (không nhận ra): Giảm confidence threshold
- **Quá lỏng lẻo** (nhận nhầm): Tăng confidence threshold

## 📊 Ví dụ dataset hoàn hảo:

### Cấu trúc folder (khuyến nghị):
```
thanh/
├── main.jpg         (mặt thẳng, ánh sáng tự nhiên)
├── side.jpg         (nghiêng phải 15°)  
├── glasses.jpg      (đeo kính)
├── smile.jpg        (cười tươi)
└── office.jpg       (ánh sáng đèn trong nhà)

Kết quả: 📁 Thanh: 5 images ⭐⭐⭐
```

### Cấu trúc file (legacy):
```
person_a.jpg         (mặt thẳng, ánh sáng tự nhiên)
person_a_1.jpg       (nghiêng phải 15°)  
person_a_2.jpg       (đeo kính)
person_a_3.jpg       (cười tươi)
person_a_4.jpg       (ánh sáng đèn trong nhà)

Kết quả: 📄 Person A: 5 images ⭐⭐⭐
```

## 🚀 Hướng dẫn nhanh:

1. **Tạo folder** tên người trong `dataset/`
2. **Copy 3-5 ảnh** chất lượng cao vào folder
3. **Chạy app** và click "Reload Faces"  
4. **Test camera** để kiểm tra độ chính xác
5. **Điều chỉnh** confidence threshold nếu cần

---

**Sau khi thêm ảnh mới, nhớ click "Reload Faces" trong ứng dụng để train lại model!**
