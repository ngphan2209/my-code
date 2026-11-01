# Kiểm kê nguồn đã đọc

Mỗi loại có một bản đính kèm trong thư mục làm việc; các hậu tố (1), (2) là tên thực tế của lần tải này. Không chọn bản chỉ dựa trên tên trong lịch sử.

| Tệp | SHA-256 |
| --- | --- |
| Code_Hệ chuyên gia tư vấn Khu du lịch miền Nam_Nhóm 1(2).rar | `a95b80b89a147d936d22f11d7dbd58308a4f4a64ded14e153fc7258e23943eb6` |
| minh hoa 30 dia diem(2).docx | `5c48bc74cd4efe8b488480dda6aaffa6acce97c1bb9f3cd8dadd48a5cb1fac3f` |
| nền sảnh(1).png | `da62bcae2621d08391aa501fb51701874cd1e36eac3e1e064185682f13766a16` |
| nền tư vấn(1).png | `09919bc680b8d8e92a4dbc53b6041308908a3a166a632b49a14e3189ce7fb553` |
| tap luat-sk 30 dia diem(1).docx | `92889c8350c45b0604e07b82a4d6ab44791c4ecccd01d21ec79de59cc7b58b71` |

## Mã nguồn cũ

Đã đọc danh sách 3.781 mục của RAR bằng libarchive; chỉ lấy nội dung mã/text ngoài .venv để tham khảo. Không kích hoạt hay dùng môi trường có sẵn trong RAR.
Đã đọc Hello.py (SanhChinh, GiaoDienTuVan), giaodientv.ui, sanhchinh.ui và các tệp giao diện Python tương ứng. image_rc.py là tài nguyên nhúng, không dùng lại.
Luồng cũ: từ sảnh mở cửa sổ tư vấn khác; chọn 5 tiêu chí; duyệt luật rồi return ở kết quả đầu tiên; thông tin và luật đặt trong lớp giao diện. Có except bỏ qua lỗi ảnh và đường dẫn dựa vào thư mục chạy.
Bản mới dùng đúng bảy nhóm từ Word mới, một cửa sổ với QStackedWidget, JSON tách riêng, kiểm tra chung và duyệt toàn bộ luật. Không tái sử dụng mã sự kiện hoặc luật của RAR.

## Tài liệu tri thức và ảnh

81 sự kiện gồm 51 mã đầu vào và 30 mã kết luận. 30 địa điểm, 435 cặp lời văn/biểu thức có số 1–435 liên tục. 30 ảnh nhúng được liên kết theo tiêu đề khối và chú thích. Hai nền được sao chép nguyên ảnh đúng vai trò.
Giữ nguyên mô tả nguồn, cả các thông tin tỉnh/khoảng cách/ngân sách; không xác minh bằng web và không sửa theo suy đoán. Phạm vi nguồn có R6 (khu vực Long An cũ) cho T27–T28; cần thuyết minh khi báo cáo đề tài ĐBSCL.

## Đối chiếu mốc ban đầu

| Mốc | Thực tế | Kết luận |
| --- | --- | --- |
| Địa điểm | 30 | Khớp |
| Luật đánh số | 435 | Khớp |
| Cặp trùng điều kiện và kết luận | 13 | Khớp |
| Luật 75 / 87 | T5 / T6, cùng điều kiện | Khớp |
| Luật 114 / 136 | T8 / T9, cùng điều kiện | Khớp |
| Lời văn K lệch ở T27–T28 | 20 | Khớp |
| Luật 380 | Lời văn K1, biểu thức K2 | Khớp |

Không phát hiện khác biệt số lượng so với các mốc người dùng cung cấp. Danh sách chi tiết cảnh báo nằm trong knowledge_audit.md.
