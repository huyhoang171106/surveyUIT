# surveyUIT

Công cụ tự động điền nhanh phiếu khảo sát môn học dành cho sinh viên trường Đại học Công nghệ Thông tin (UIT).

## Các tính năng chính

1. **Hỗ trợ đa nền tảng**: Hoạt động ổn định trên cả Windows và Linux. Tự động thiết lập encoding UTF-8 để hiển thị tiếng Việt chính xác trên console.
2. **Tự động điền thông tin tối ưu**: Tự động trả lời theo các tiêu chuẩn mặc định:
   - Học lực: Giỏi
   - Tỷ lệ lên lớp: >80%
   - Đạt chuẩn đầu ra: Trên 90%
   - Đánh giá giảng viên: 4 điểm cho tất cả tiêu chí
   - Các ý kiến đóng góp khác: Để trống
3. **Tự động quét danh sách từ Portal**: Đăng nhập qua Session Cookie, tự động tìm kiếm các khảo sát chưa hoàn thành trên Portal sinh viên, lọc bỏ các link đã hoàn thành và tự động đổi giao thức sang HTTPS.
4. **Hỗ trợ đa luồng**: Sử dụng ThreadPoolExecutor thực hiện gửi khảo sát song song tối đa 4 luồng giúp hoàn thành công việc nhanh chóng.

## Hướng dẫn cài đặt

Cài đặt thư viện requests trước khi chạy chương trình:

```bash
pip install requests
```

## Hướng dẫn sử dụng

### Cách 1: Quét trực tiếp từ Portal Sinh viên (Khuyên dùng)

Lấy Cookie của trang Portal Sinh viên `student.uit.edu.vn` (F12 -> Application -> Cookies -> tìm khóa `SSESS...`), sau đó chạy lệnh sau:

```bash
python surveyUIT.py "https://student.uit.edu.vn/sinhvien/phieukhaosat?destination=sinhvien/phieukhaosat" "SSESSdf6f777d3f8a1d0fb2e4e5d1ec62f6e2=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Cách 2: Sử dụng danh sách link từ file văn bản

Tạo một file text chứa danh sách các link khảo sát (ví dụ `links.txt`, mỗi link một dòng), sau đó chạy lệnh:

```bash
python surveyUIT.py links.txt
```

## Bản quyền & Đóng góp
- Phát triển bởi Truoc Phan (truocphan112017@gmail.com).
- Cập nhật và tối ưu hóa hiệu năng bởi Huy Hoang.
